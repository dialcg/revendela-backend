import pytest
from rest_framework.test import APIClient
from events.models import EventCategory, Organizer, Venue
from tickets.models import Event
from django.urls import reverse


@pytest.mark.django_db
def test_get_event_list_api_view():
    client = APIClient()

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

    url = reverse("event-list")
    response = client.get(url)

    assert response.status_code == 200
    assert response.data["count"] == 2  
    assert len(response.data["results"]) == 2
    
@pytest.mark.django_db
def test_get_event_list_api_view_no_events():
    client = APIClient()

    url = reverse("event-list")
    response = client.get(url)

    assert response.status_code == 200
    assert response.data["count"] == 0 
    assert len(response.data["results"]) == 0 