from django.urls import path
from core.views import *

urlpatterns = [
    path("onboard-app", onboarding_view, name="onboard-app")
]