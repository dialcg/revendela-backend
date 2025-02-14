from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    BUYER = "buyer"
    SELLER = "seller"
    ROLE_CHOICES = [
        (BUYER, "Comprador"),
        (SELLER, "Vendedor"),
    ]

    profile_picture = models.ImageField(
        upload_to="profile_pictures/", blank=True, null=True
    )
    social_account_provider = models.CharField(max_length=50, blank=True, null=True)
    role = models.CharField(
        max_length=10, choices=ROLE_CHOICES, blank=False, null=False
    )

    def __str__(self):
        return self.username

class Wallet(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="wallet")
    balance = models.DecimalField(max_digits=10, decimal_places=3, default=0.000)
    last_updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Wallet"
        verbose_name_plural = "Wallets"

    def __str__(self):
        return f"{self.user.username} - Balance: {self.balance}"