import pytest
from django.urls import reverse
from authy.models import CustomUser
from django.contrib.messages import get_messages
from events.models import EventCategory, Organizer, Venue
from payments.tests.test_views import User
from tickets.models import Event, Ticket
from events.repositories import EventRepository


@pytest.mark.django_db
def test_get_context_data(client):
    user = User.objects.create_user(username="seller", password="password", role="seller")
    client.login(username="seller", password="password")  

    category = EventCategory.objects.create(name="Music")
    venue = Venue.objects.create(name="Stadium", address="123 Street")
    organizer = Organizer.objects.create(name="EventCorp")

    event1 = Event.objects.create(
        name="Concert",
        date="2025-05-01",
        category=category,
        venue=venue,
        organizer=organizer,
    )
    event2 = Event.objects.create(
        name="Conference",
        date="2025-06-01",
        category=category,
        venue=venue,
        organizer=organizer,
    )

    EventRepository.get_all_events = lambda: [event1, event2]

    url = reverse("ticket_sale_view")
    response = client.get(url)

    assert response.status_code == 200 



@pytest.mark.django_db
def test_post_successfully(client):

    user = CustomUser.objects.create_user(
        username="testbuyer", password="password", role=CustomUser.SELLER
    )
    client.login(username="testbuyer", password="password")

    category = EventCategory.objects.create(name="Music")
    venue = Venue.objects.create(name="Stadium", address="123 Street")
    organizer = Organizer.objects.create(name="EventCorp")

    event = Event.objects.create(
        name="Concert",
        date="2025-05-01",
        category=category,
        venue=venue,
        organizer=organizer,
    )

    EventRepository.get_event_by_id = lambda id: event

    url = reverse("ticket_sale_view")
    response = client.post(
        url,
        {
            "event": event.id,
            "resale_price": 100,
            "venue_location": "General",
            "purchase_status": "AVAILABLE",
        },
    )

    assert Ticket.objects.count() == 1
    messages = list(get_messages(response.wsgi_request))
    assert str(messages[0]) == "Se ha creado exitosamente el ticket"
