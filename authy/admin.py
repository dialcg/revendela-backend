from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Wallet


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ("username", "email", "role", "is_active", "is_staff")
    search_fields = ("username", "email")
    list_filter = ("role", "is_active", "is_staff")
    fieldsets = UserAdmin.fieldsets + (
        ("Additional Info", {"fields": ("profile_picture", "social_account_provider", "role")}),
    )


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ("user", "formatted_balance", "last_updated_at")
    search_fields = ("user__username",)
    ordering = ("-last_updated_at",)

    def formatted_balance(self, obj):
        return "{:,.0f}".format(obj.balance)
    formatted_balance.short_description = 'Balance'

