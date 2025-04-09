import json
import requests
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.clickjacking import xframe_options_exempt
from django.conf import settings
from .models import PaymentIntegration


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
    # payload = {
    #         'merchant_id': merchant_id,
    #         'ref_number': charge_id,
    #         'transaction_id': transaction_id,
    #         'api_key': api_key
    #     }
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
        # payload = {
        #     'merchant_id': 'f6e5c7acb12cc27c3f7deef92831d590',
        #     'ref_number': '641368878',
        #     'transaction_id': '393a93d21eb84764',
        #     'api_key': 'db8a2e2842e3980e182cd510f509bf47fd92bb4167e6cbc257d09bf9cc97d6f1'
        # }
        print("payload:",json.dumps(payload,indent=4))
        response = requests.post(verification_url, data=payload, timeout=10)
        response.raise_for_status()
        response_data = response.json()
        print("response:",json.dumps(response_data,indent=4))
    except requests.RequestException as e:
        print("HTTP Request failed:", str(e))
        return JsonResponse({'error': 'Payment verification failed'}, status=400)
    except ValueError:
        return JsonResponse({'error': 'Invalid response from payment server'}, status=400)
    # return JsonResponse({"success": True, "data": payload})
    if response_data.get('status') == 'success':
        print("Transaction verified successfully:", response_data.get('data'))
        return JsonResponse({"success": True, "data": response_data.get('data')},status=200)
    else:
        print("Verification failed:", response_data.get('message'))
        return JsonResponse({"failed": True, "message": response_data.get('message'),},status=400)