from django.contrib import admin
from django.utils.html import format_html
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
        'updated_at',
        'image_thumbnail',  # add thumbnail column
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
                ("Credentials - Live", {
                    "fields": ("live_apikey", "live_publishablekey")
                }),
                ("Credentials - Test", {
                    "fields": ("test_apikey", "test_publishablekey")
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
                    "fields": (
                        "name", "description",
                        "image_url", "query_url", "payments_url",
                        "live_apikey", "live_publishablekey",
                        "test_apikey", "test_publishablekey",
                    )
                }),
            )

    def image_thumbnail(self, obj):
        if obj.image_url:
            return format_html('<img src="{}" width="50" height="50" style="object-fit:cover;border-radius:4px;" />', obj.image_url)
        return "-"
    image_thumbnail.short_description = 'Image'
