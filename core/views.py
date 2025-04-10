from django.shortcuts import render
from core.services import OAuthServices


def onboarding_view(request):
    auth_code = request.GET.get("code")

    if auth_code:
        OAuthServices.get_fresh_token(auth_code)
        

    return render(request, 'onboard.html', {
        "auth_code": auth_code,
        "client_id": "67f432dab0c46a706b85044d-m97lqtnn",
        "redirect_uri": "http://localhost:8000/core/onboard-app",
        "is_loading": False
    })