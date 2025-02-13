from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Ticket

def send_ticket_email(subject, message, recipient_email):
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [recipient_email],
        fail_silently=False,
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