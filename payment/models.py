from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

def validate_https_url(value):
    if not value.startswith('https://'):
        raise ValidationError('Only HTTPS URLs are allowed.')

class PaymentIntegration(models.Model):
    ghl_id = models.CharField(max_length=100, unique=True, blank=True, null=True)  # _id from GHL
    location_id = models.CharField(max_length=100, blank=True, null=True)
    marketplace_app_id = models.CharField(max_length=100, blank=True, null=True)

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)


    image_url = models.URLField(
      
       
    )
    query_url = models.URLField(
        validators=[validate_https_url],
        help_text="Enter the query endpoint URL (must start with https://)."
    )
    payments_url = models.URLField(
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
