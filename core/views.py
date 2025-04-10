from django.shortcuts import render, redirect
from core.services import OAuthServices
from django.urls import reverse
from django.conf import settings



def onboarding_view(request):
    auth_code = request.GET.get("code")

    if auth_code:
        token = OAuthServices.get_fresh_token(auth_code)
        if token:
            return redirect(f'payment_integration_create', chr=token.LocationId)

    return render(request, 'onboard.html', {
        "auth_code": auth_code,
        "client_id": settings.CLIENT_ID,
        "redirect_uri": settings.REDIRECT_URI,
        "is_loading": False
    })