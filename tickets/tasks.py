from celery import shared_task
from datetime import timedelta
from django.utils import timezone
from tickets.models import Ticket

@shared_task
def cancel_pending_tickets_task():
    cutoff = timezone.now() - timedelta(hours=48)
    tickets_to_cancel = Ticket.objects.filter(
        purchase_status=Ticket.PENDING,
        last_status_change__lte=cutoff
    )

    count = tickets_to_cancel.update(purchase_status=Ticket.CANCELLED_SELLER)
    print(f"{count} ticket(s) cancelados por estar pendientes más de 48 horas.")
