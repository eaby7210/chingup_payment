import json
import requests
from django.db import transaction
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.clickjacking import xframe_options_exempt
from django.conf import settings
from .models import PaymentIntegration, PaymentVerificationLog, IframeEventLogs
from .forms import PaymentIntegrationForm
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
from core.services import OAuthServices,OAuthTokenError
from core.models import OAuthToken
from django.contrib import messages
from .services import GHLCustomProviderServices


@csrf_exempt
@xframe_options_exempt
def payment_view(request):
    if request.method == "POST":
        data =json.loads(request.body)
        
        print(json.dumps(data, indent=4))
        
        return render(request,"payframe.html",data)
    elif request.method =='GET':
        data={
            'merchant_id':settings.CHINGUP_MERCHANT_SANDBOX_ID
        }
        return render(request,"payframe.html",data)

@csrf_exempt
def payment_verify(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=405)

    try:
        data = json.loads(request.body)
        print("Received Payload:", json.dumps(data, indent=4))
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    api_key = data.get("apiKey") or data.get("apikey")
    charge_id = data.get("chargeId")
    transaction_id = data.get("transactionId")

    if not api_key or not charge_id or not transaction_id:
        return JsonResponse({'error': 'Missing required fields'}, status=400)

    # Try to fetch the payment integration using live or test keys
    integration = PaymentIntegration.objects.filter(live_apikey=api_key).first()
    is_live = True

    if not integration:
        integration = PaymentIntegration.objects.filter(test_apikey=api_key).first()
        is_live = False
    if is_live:
        url='https://chingup.com/api/verify_transaction/'
    else:
        url='https://chingup.com/api/sandbox/verify_transaction/'
    if not integration:
        return JsonResponse({'error': 'Invalid API key'}, status=403)

    merchant_id = (
        integration.live_publishablekey if is_live else integration.test_publishablekey
    )
    log = PaymentVerificationLog.objects.create(
        request_payload=data,
        api_key=api_key,
        charge_id=charge_id,
        transaction_id=transaction_id,
        is_live=is_live,
        merchant_id=merchant_id,
    )
    # print("payload:",json.dumps(payload,indent=4))
    # Call external verification API
    try:
        print(f"using url: {url}")
        verification_url = url
        payload = {
            'merchant_id': merchant_id,
            'ref_number': charge_id,
            'transaction_id': transaction_id,
            'api_key': api_key
        }

        print("payload:",json.dumps(payload,indent=4))
        response = requests.post(verification_url, data=payload, timeout=10)
        response.raise_for_status()
        response_data = response.json()
        print("response:",json.dumps(response_data,indent=4))
    except requests.RequestException as e:
        msg = f"HTTP Request failed: {str(e)}"
        print(msg)
        log.response_data = str(e)
        log.success = False
        log.error_message = msg
        log.save()
        return JsonResponse({'error': 'Payment verification failed'}, status=400)
    except ValueError as e:
        msg = f"Invalid response from payment server: {str(e)}"
        log.response_data = str(e)
        log.success = False
        log.error_message = msg
        log.save()
        return JsonResponse({'error': 'Invalid response from payment server'}, status=400)

    log.response_data = response_data
    log.success = response_data.get('status') == 'success'
    log.error_message = response_data.get('message') if not log.success else None
    log.save()
    
    if response_data.get('status') == 'success':
        print("Transaction verified successfully:", response_data.get('data'))
        return JsonResponse({"success": True, "data": response_data.get('data')},status=200)
    else:
        print("Verification failed:", response_data.get('message'))
        return JsonResponse({"failed": True, "message": response_data.get('message'),},status=400)
    



def configure_provider(instance):
    """
    Configure provider credentials (live and test).
    """
    credential_payload = {
        "live": {
            "apiKey": instance.live_apikey,
            "publishableKey": instance.live_publishablekey,
        },
        "test": {
            "apiKey": instance.test_apikey,
            "publishableKey": instance.test_publishablekey,
        }
    }

    config_response = GHLCustomProviderServices.create_provider_config(payload=credential_payload)
    if not config_response:
        raise ValueError("Failed to configure provider credentials.")


def create_or_update_custom_provider(instance):
    """
    Creates or updates a GHL custom payment provider and configures credentials.
    """
    provider_payload = {
        "name": instance.name,
        "description": instance.description,
        "paymentsUrl": instance.payments_url,
        "queryUrl": instance.query_url,
        "imageUrl": instance.image_url,
    }

    response = GHLCustomProviderServices.create_custom_provider_integration(data=provider_payload)
    if not response:
        raise ValueError("Failed to create or update custom provider integration.")

    # Map response to model instance fields
    instance.ghl_id = response.get("_id")
    instance.location_id = response.get("locationId")
    instance.marketplace_app_id = response.get("marketplaceAppId")
    instance.trace_id = response.get("traceId")
    instance.deleted = response.get("deleted", False)

    provider_config = response.get("providerConfig", {})
    instance.live_mode = provider_config.get("live", {}).get("liveMode")
    instance.test_mode = provider_config.get("test", {}).get("liveMode")

    # Save updated instance fields
    instance.save()

    # Configure credentials
    configure_provider(instance)


def payment_integration_create_view(request, location_id):
    """
    View to handle creation of a new payment integration.
    """
    form = PaymentIntegrationForm(request.POST or None)
    
    if request.method == 'POST':
        print("form: ", form)
        if form.is_valid():
            print("valid form in post")
            try:
                with transaction.atomic():
                    instance = form.save(commit=False)
                    instance.save()
                    create_or_update_custom_provider(instance)
                request.session['onboarding_success'] = True
                return redirect('payment_integration_success')
            except Exception as e:
                form.add_error(None, str(e))
                
        print("form 2=============: ", form)
        return render(request, 'payment_integration_form.html', {
            'form': form,
            })
            
        
        
    elif request.method =='GET':
        if not request.session.pop('onboarding_redirect',None):
            return redirect("onboard-app")
        else:
            print("Redirected")
        try:
            token_obj:OAuthToken = OAuthServices.get_valid_access_token_obj()
        except OAuthTokenError as e:
            messages.error(request,str(e))
            return redirect("onboard-app")
            
        form = PaymentIntegrationForm()
        if token_obj and token_obj.LocationId ==location_id:
            print(f"Valid Location{token_obj.LocationId}")
            return render(request, 'payment_integration_form.html', {
            'form': form,
        })
        else:
            print("Invalid token")
            return redirect("onboard-app")
        

def payment_integration_success_view(request):
    print("payment_integration_success")
    return render(request, 'payment_integration_success.html')

@csrf_exempt
@xframe_options_exempt
def log_iframe_event(request):
    if request.method == "POST":
        try:
            payload = json.loads(request.body)
            print("Received Payload:", json.dumps(payload, indent=4))
            event_type = payload.get("event_type", "unknown")
            data = payload.get("data", {})

            IframeEventLogs.objects.create(
                event_type=event_type,
                data=data
            )
            return JsonResponse({"message": "Logged successfully"}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)