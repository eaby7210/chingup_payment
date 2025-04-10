from django import forms
from .models import PaymentIntegration


class PaymentIntegrationForm(forms.ModelForm):
    class Meta:
        model = PaymentIntegration
        fields = [
        
        'live_apikey', 'live_publishablekey',
        'test_apikey', 'test_publishablekey'
    ]

    # readonly_fields = [
    #     'ghl_id', 'location_id', 'marketplace_app_id',
    #     'trace_id', 'created_at', 'updated_at'
    # ]

    # create_only_fields = [
    #     'name', 'description',
    #     'image_url', 'query_url', 'payments_url',
    #     'live_apikey', 'live_publishablekey',
    #     'test_apikey', 'test_publishablekey'
    # ]

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)

    #     # Always disable readonly fields
    #     for field in self.readonly_fields:
    #         if field in self.fields:
    #             self.fields[field].disabled = True

    #     # If creating a new instance, hide non-create-only fields
    #     if not self.instance or not self.instance.pk:
    #         for field_name in self.fields:
    #             if field_name not in self.create_only_fields and field_name not in self.readonly_fields:
    #                 self.fields[field_name].widget = forms.HiddenInput()
