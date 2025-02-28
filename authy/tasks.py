from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from authy.models import CustomUser
from tickets.models import Ticket

@shared_task
def deactivate_inactive_users_task():
    threshold_date = timezone.now() - timedelta(days=30)
    active_users = CustomUser.objects.filter(is_active=True)

    for user in active_users:
        user_tickets = Ticket.objects.filter(seller=user)
        if not user_tickets.exists() and user.date_joined < threshold_date:
            user.is_active = False
            user.save()
