from celery import shared_task
from datetime import timedelta
from django.utils import timezone
from tickets.models import Ticket
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def cancel_pending_tickets_task():
    cutoff = timezone.now() - timedelta(hours=48)
    tickets_to_cancel = Ticket.objects.filter(
        purchase_status=Ticket.PENDING,
        last_status_change__lte=cutoff
    )

    count = tickets_to_cancel.update(purchase_status=Ticket.CANCELLED_SELLER)
    print(f"{count} ticket(s) cancelados por estar pendientes más de 48 horas.")

@shared_task
def notify_buyer_of_sold_tickets_task():
    cutoff = timezone.now() - timedelta(hours=24)
    sold_tickets = Ticket.objects.filter(
        purchase_status=Ticket.SOLD,
        last_status_change__lte=cutoff
    )

    for ticket in sold_tickets:
        if ticket.buyer and ticket.buyer.email:
            send_mail(
                'Compra de entrada',
                f'Hola {ticket.buyer.username}, tu entrada para el evento {ticket.event.name} ha sido vendida.',
                settings.DEFAULT_FROM_EMAIL,
                [ticket.buyer.email],
                fail_silently=False,
            )
    print(f"Notificaciones enviadas a los compradores de {sold_tickets.count()} ticket(s) vendidos.")

@shared_task
def cancel_unsold_tickets_after_event_end_task():
    now = timezone.now()
    tickets_to_cancel = Ticket.objects.filter(
        purchase_status=Ticket.AVAILABLE,
        event__end_datetime__lte=now
    )

    count = tickets_to_cancel.update(purchase_status=Ticket.CANCELLED_EVENT_TIME)
    print(f"{count} ticket(s) cancelados por no venderse antes de la hora final del evento.")
