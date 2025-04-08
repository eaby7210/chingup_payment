from django.contrib import admin
from .models import PaymentIntegration

@admin.register(PaymentIntegration)
class PaymentIntegrationAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'location_id',
        'marketplace_app_id',
        'live_mode',
        'test_mode',
        'deleted',
        'updated_at'
    )
    list_filter = ('live_mode', 'test_mode', 'deleted', 'created_at')
    search_fields = ('name', 'location_id', 'marketplace_app_id', 'ghl_id', 'trace_id')
    
    readonly_fields = ('created_at', 'updated_at', 'ghl_id', 'location_id', 'marketplace_app_id', 'trace_id')

    def get_fieldsets(self, request, obj=None):
        if obj:  # editing existing object
            return (
                ("Basic Info", {
                    "fields": ("name", "description", "ghl_id", "location_id", "marketplace_app_id")
                }),
                ("URLs", {
                    "fields": ("image_url", "query_url", "payments_url")
                }),
                ("Mode Settings", {
                    "fields": ("live_mode", "test_mode", "deleted")
                }),
                ("System Fields", {
                    "fields": ("trace_id", "created_at", "updated_at")
                }),
            )
        else:  # adding a new object
            return (
                ("Create Payment Integration", {
                    "fields": ("name", "description", "image_url", "query_url", "payments_url")
                }),
            )
