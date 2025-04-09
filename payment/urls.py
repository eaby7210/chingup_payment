from django.urls import path
from payment.views import *

urlpatterns = [
    path("payment-verify/", payment_verify, name="payment-verify")
]