from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import PaymentIntegration
from payment.services import GHLCustomProviderServices 



@receiver(pre_save, sender=PaymentIntegration)
def create_custom_provider_signal(sender, instance, **kwargs):
 
    if instance.pk:
   
        try:
            existing = PaymentIntegration.objects.get(pk=instance.pk)
            if existing.ghl_id:
                raise ValueError("Cannot update a PaymentIntegration once it has been synced with GHL.")
        except PaymentIntegration.DoesNotExist:
            pass  

    # Only sync if it's a new entry (no ghl_id)
    if not instance.ghl_id:
        payload = {
            "name": instance.name,
            "description": instance.description,
            "paymentsUrl": instance.payments_url,
            "queryUrl": instance.query_url,
            "imageUrl": instance.image_url,
        }

        response = GHLCustomProviderServices.create_custom_provider_integration(data=payload)

        if response:
            instance.ghl_id = response.get("_id")
            instance.location_id = response.get("locationId")
            instance.marketplace_app_id = response.get("marketplaceAppId")
            instance.trace_id = response.get("traceId")
            instance.deleted = response.get("deleted", False)

            provider_config = response.get("providerConfig", {})
            instance.live_mode = provider_config.get("live", {}).get("liveMode")
            instance.test_mode = provider_config.get("test", {}).get("liveMode")
