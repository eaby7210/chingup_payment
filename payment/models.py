from django.db import models
from django.utils import timezone
from django.conf import settings
from django.core.exceptions import ValidationError

def validate_https_url(value):
    if not value.startswith('https://'):
        raise ValidationError('Only HTTPS URLs are allowed.')

class PaymentIntegration(models.Model):
    ghl_id = models.CharField(max_length=100, unique=True, blank=True, null=True)  # _id from GHL
    location_id = models.CharField(max_length=100, blank=True, null=True)
    marketplace_app_id = models.CharField(max_length=100, blank=True, null=True)

    name = models.CharField(max_length=255,default=settings.NAME)
    description = models.TextField(default=settings.DESCRIPTION,blank=True, null=True)


    image_url = models.URLField(default=settings.IMAGE_URL,
      
       
    )
    query_url = models.URLField(default=settings.QUERY_URL,
        validators=[validate_https_url],
        help_text="Enter the query endpoint URL (must start with https://)."
    )
    payments_url = models.URLField(default=settings.PAYMENT_URL,
        validators=[validate_https_url],
        help_text="Enter the payments endpoint URL (must start with https://)."
    )

    live_apikey = models.CharField(max_length=255, blank=True, null=True)
    live_publishablekey = models.CharField(max_length=255,
                                           blank=True, null=True,
                                           help_text="For ChingUp You can add Merchant Id.")
    test_apikey = models.CharField(max_length=255, blank=True, null=True)
    test_publishablekey = models.CharField(max_length=255,
                                           blank=True, null=True,
                                           help_text="For ChingUp You can add Merchant Id.")


    live_mode = models.BooleanField(blank=True, null=True)
    test_mode = models.BooleanField(blank=True, null=True)

    deleted = models.BooleanField(blank=True, null=True)
    trace_id = models.CharField(max_length=255, blank=True, null=True)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Payment Integration"
        verbose_name_plural = "Payment Integrations"

    def __str__(self):
        return f"{self.name} ({self.location_id})"


class PaymentVerificationLog(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    is_live = models.BooleanField(default=False)


    request_payload = models.JSONField()
    api_key = models.CharField(max_length=255)
    charge_id = models.CharField(max_length=255, null=True, blank=True)
    transaction_id = models.CharField(max_length=255)


    merchant_id = models.CharField(max_length=255)

    response_data = models.JSONField(null=True, blank=True)
    success = models.BooleanField(default=False)
    error_message = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.timestamp} | {self.transaction_id} | {'LIVE' if self.is_live else 'TEST'}"


class IframeEventLogs(models.Model):
    event_type = models.CharField(max_length=100)
    data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.event_type} at {self.created_at}"