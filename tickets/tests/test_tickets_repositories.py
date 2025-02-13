import pytest
from events.models import Event, EventCategory, Organizer
from authy.models import CustomUser
from decimal import Decimal
from tickets.models import Ticket
from tickets.repositories import TicketRepository


@pytest.mark.django_db
def test_create_ticket_success():

    category = EventCategory(name="Music")
    category.save()
    organizer = Organizer(name="BlackMusic")
    organizer.save()
    event = Event(name="Concert", category=category, organizer=organizer)
    event.save()
    user = CustomUser.objects.create_user(username="seller1", password="password123")

    resale_price = Decimal("100.50")
    venue_location = "VIP ANYTIME"
    purchase_status = Ticket.AVAILABLE
    ticket = TicketRepository.create_ticket(
        event=event,
        resale_price=resale_price,
        venue_location=venue_location,
        purchase_status=purchase_status,
        seller=user,
    )

    assert Ticket.objects.all().count() == 1
