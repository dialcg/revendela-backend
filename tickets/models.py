import uuid
from django.db import models
from authy.models import CustomUser
from events.models import Event


class Ticket(models.Model):

    AVAILABLE = "AVAILABLE"
    PENDING = "PENDING"
    SOLD = "SOLD"
    SENT = "SENT"
    CLOSED = "CLOSED"
    CANCELLED_SELLER = "CANCELLED_SELLER"

    STATUS_CHOICES = [
        (AVAILABLE, "Disponible"),
        (PENDING, "Pendiente"),
        (SOLD, "Vendido"),
        (SENT, "Enviado"),
        (CLOSED, "Cerrado"),
        (CANCELLED_SELLER, "Cancelado"),
    ]

    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, blank=False, null=False, related_name="Evento"
    )
    unique_identifier = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    resale_price = models.DecimalField(
        max_digits=10,
        decimal_places=3,
        blank=True,
        null=True,
        verbose_name="Precio de reventa",
    )
    purchase_status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default=AVAILABLE, blank=True, null=True
    )
    seller = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name="Vendedor",
    )
    buyer = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="Comprador",
    )
    venue_location = models.CharField(
        max_length=100, null=False, blank=False, verbose_name="Locacion"
    )
    last_status_change = models.DateTimeField(
        verbose_name="Último cambio de estado",
        null=False,
        blank=False
    )

    class Meta:
        verbose_name = "Ticket"
        verbose_name_plural = "Tickets"
        ordering = ["event", "unique_identifier"]

    def __str__(self):
        return f"Ticket {self.unique_identifier} for {self.event.name}"
