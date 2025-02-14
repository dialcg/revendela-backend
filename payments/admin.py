from django.contrib import admin
from .models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("uuid", "user", "amount", "status", "created_at")
    search_fields = ("uuid", "reference", "wompi_id", "user__username")
    list_filter = ("status", "created_at")
    ordering = ("-created_at",)
