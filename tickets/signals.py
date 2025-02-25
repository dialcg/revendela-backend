import logging
from decimal import Decimal
from django.db import transaction
from django.db.models import F
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from .models import Ticket
from authy.models import Wallet

def send_ticket_email(subject, message, recipient_email):
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [recipient_email],
        fail_silently=False,
    )
    
logger = logging.getLogger(__name__)

@receiver(post_save, sender=Ticket)
def update_last_status_change(sender, instance, **kwargs):
    update_fields = kwargs.get('update_fields')

    if update_fields and 'status' in update_fields:
        try:
            with transaction.atomic():
                instance.last_status_change = timezone.now()
                instance.save(update_fields=['last_status_change'])
                logger.info(
                    f"Updated last_status_change for ticket {instance.unique_identifier}."
                )
        except Exception as e:
            logger.error(
                f"Error updating last_status_change for ticket {instance.unique_identifier}: {str(e)}"
            )


@receiver(post_save, sender=Ticket)
def notify_ticket_status_change(sender, instance, **kwargs):
    if instance.purchase_status == Ticket.SENT and instance.buyer:
        subject = "Tu ticket ha sido enviado"
        message = (
            f"Hola {instance.buyer.first_name},\n\n"
            f"El ticket {instance.unique_identifier} para el evento {instance.event.name} ha sido enviado.\n"
            f"Ubicación: {instance.venue_location}.\n\n"
            "Gracias por tu compra."
        )
        send_ticket_email(subject, message, instance.buyer.email)
    
    elif instance.purchase_status == Ticket.CLOSED and instance.seller:
        subject = "Tu ticket ha sido cerrado"
        message = (
            f"Hola {instance.seller.first_name},\n\n"
            f"El ticket {instance.unique_identifier} para el evento {instance.event.name} ha sido marcado como CERRADO.\n"
            "Gracias por usar nuestra plataforma."
        )
        send_ticket_email(subject, message, instance.seller.email)
        
        try:
            with transaction.atomic():
                amount_after_fee = Decimal(str(instance.resale_price)) * Decimal("0.92")

                seller_wallet, created = Wallet.objects.get_or_create(
                    user=instance.seller, defaults={"balance": Decimal("0.00")}
                )

                seller_wallet.balance += amount_after_fee
                seller_wallet.save()

                logger.info(
                    f"Billetera de {instance.seller.username} actualizada con ${amount_after_fee} después de la tarifa del 8%."
                )

        except Exception as e:
            logger.error(
                f"Error al actualizar la billetera del vendedor {instance.seller.username}: {str(e)}"
            )