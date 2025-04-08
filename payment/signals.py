from django.db import transaction
from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import PaymentIntegration
from .services import GHLCustomProviderServices


@receiver(pre_save, sender=PaymentIntegration)
def create_or_update_custom_provider_signal(sender, instance, **kwargs):
    with transaction.atomic():
  
        provider_payload = {
            "name": instance.name,
            "description": instance.description,
            "paymentsUrl": instance.payments_url,
            "queryUrl": instance.query_url,
            "imageUrl": instance.image_url,
        }

        response = GHLCustomProviderServices.create_custom_provider_integration(data=provider_payload)

        if not response:
            raise ValueError("Failed to create or update custom provider integration.")

        instance.ghl_id = response.get("_id")
        instance.location_id = response.get("locationId")
        instance.marketplace_app_id = response.get("marketplaceAppId")
        instance.trace_id = response.get("traceId")
        instance.deleted = response.get("deleted", False)

        provider_config = response.get("providerConfig", {})
        instance.live_mode = provider_config.get("live", {}).get("liveMode")
        instance.test_mode = provider_config.get("test", {}).get("liveMode")

        credential_payload = {
            "live": {
                "apiKey": instance.live_apikey,
                "publishableKey": instance.live_publishablekey,
            },
            "test": {
                "apiKey": instance.test_apikey,
                "publishableKey": instance.test_publishablekey,
            }
        }

        config_response = GHLCustomProviderServices.create_provider_config(payload=credential_payload)

        if not config_response:
            raise ValueError("Failed to configure provider credentials.")
