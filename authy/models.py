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
