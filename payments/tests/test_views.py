import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from events.models import Event, EventCategory, Venue, Organizer
from tickets.models import Ticket
from payments.models import Transaction
from decimal import Decimal
from uuid import uuid4

User = get_user_model()


@pytest.mark.django_db
def test_post_transaction_success():
    client = APIClient()
    user = User.objects.create_user(
        username="testuser", password="password123", email="testuser@example.com"
    )
    client.force_authenticate(user=user)

    category = EventCategory.objects.create(name="Conciertos")
    venue = Venue.objects.create(name="Teatro Central", address="Calle 123")
    organizer = Organizer.objects.create(name="Organizador Test")

    event = Event.objects.create(
        name="Test Event",
        description="Evento de prueba",
        category=category,
        venue=venue,
        organizer=organizer,
    )

    ticket = Ticket.objects.create(
        unique_identifier=uuid4(),
        resale_price=Decimal("100.00"),
        purchase_status=Ticket.AVAILABLE,
        seller=user,
        event=event,
        venue_location="Test Location",
    )

    wompi_id = "wompi123"
    reference = f"{ticket.unique_identifier}_12345"
    payload = {
        "wompi_id": wompi_id,
        "amount": "10000",
        "reference": reference,
        "status": "approved",
    }

    response = client.post("/wompi/transaction/", payload, format="json")

    assert response.data["message"] == "¡Ticket comprado con éxito!"

    transaction = Transaction.objects.filter(wompi_id=wompi_id).first()
    assert transaction is not None
    assert transaction.amount == Decimal("100.00")
    assert transaction.user == user

    ticket.refresh_from_db()
    assert ticket.purchase_status == Ticket.SOLD
    assert ticket.buyer == user
