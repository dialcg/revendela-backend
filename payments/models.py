import uuid
from django.db import models
from authy.models import CustomUser


class Transaction(models.Model):
    WOMPI_PENDING = "PENDING"
    WOMPI_APPROVED = "APPROVED"
    WOMPI_DECLINED = "DECLINED"
    WOMPI_VOIDED = "VOIDED"
    WOMPI_ERROR = "ERROR"

    STATUS_CHOICES = [
        (WOMPI_PENDING, "Pending"),
        (WOMPI_APPROVED, "Approved"),
        (WOMPI_DECLINED, "Declined"),
        (WOMPI_VOIDED, "Voided"),
        (WOMPI_ERROR, "Error"),
    ]

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    wompi_id = models.CharField(max_length=100, null=True, blank=True)
    reference = models.CharField(max_length=100, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=3)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=WOMPI_PENDING,
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(CustomUser, on_delete=models.PROTECT)

    def __str__(self):
        return f"Transaccion {self.uuid} - {self.status}"
