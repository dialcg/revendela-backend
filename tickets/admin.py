from django.contrib import admin
from .models import Ticket


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ("unique_identifier", "event", "seller", "buyer", "formatted_resale_price", "purchase_status", "venue_location", "last_status_change")
    search_fields = ("unique_identifier", "event__name", "seller__username", "buyer__username", "last_status_change")
    list_filter = ("purchase_status", "event")
    ordering = ("event", "unique_identifier")

    def formatted_resale_price(self, obj):
        return "{:,.0f}".format(obj.resale_price)
    formatted_resale_price.short_description = 'Resale Price'
