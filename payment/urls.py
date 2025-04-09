from django.urls import path
from . import views


urlpatterns = [
    path("payment/", views.payment_view, name="payment_iframe"),
    path("verify-payment/", views.payment_verify, name="verify_payment"),
]
