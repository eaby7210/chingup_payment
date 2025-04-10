from django.shortcuts import render, redirect
from core.services import OAuthServices
from django.urls import reverse
from django.conf import settings
from django.http import JsonResponse
import json



def onboarding_view(request):
    auth_code = request.GET.get("code")
    context = {
        "client_id": settings.CLIENT_ID,
        "redirect_uri": settings.REDIRECT_URI,
        "is_loading": False,
        "base_api_url": settings.BASE_API_URL,
    }
    if auth_code:
        token = OAuthServices.get_fresh_token(auth_code)

        if token:
            request.session['onboarding_redirect'] = True
            return redirect(f'payment_integration_create', location_id=token.LocationId)

    return render(request, 'onboard.html',context)


def save_configuration(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            location_id = data.get('loationId')
            print("location ID: ", location_id)


            if not location_id:
                return JsonResponse({'message': 'Location ID is required'}, status=400)


            return JsonResponse({'message': 'Configuration saved successfully'}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON payload'}, status=400)
        except Exception as e:
            return JsonResponse({'message': f'An error occurred: {str(e)}'}, status=500)

    return JsonResponse({'message': 'Method not allowed'}, status=405)