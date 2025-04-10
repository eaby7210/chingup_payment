from django.urls import path
from . import views


urlpatterns = [
     path('integration/create/<str:location_id>/', views.payment_integration_create_view, name='payment_integration_create'),
    path("payment/", views.payment_view, name="payment_iframe"),
    path("verify-payment/", views.payment_verify, name="verify_payment"),
    path('integration/success/', views.payment_integration_success_view, name='payment_integration_success'),
]
