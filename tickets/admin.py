from django.contrib import admin
from .models import Ticket


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ("unique_identifier", "event", "seller", "buyer", "resale_price", "purchase_status")
    search_fields = ("unique_identifier", "event__name", "seller__username", "buyer__username")
    list_filter = ("purchase_status", "event")
    ordering = ("event", "unique_identifier")
