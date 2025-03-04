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
        start_datetime="2025-05-01T20:00:00Z",
        end_datetime="2025-05-01T23:00:00Z",
        category=category,
        venue=venue,
        organizer=organizer,
    )
    event2 = Event.objects.create(
        name="Conference",
        start_datetime="2025-06-01T09:00:00Z",
        end_datetime="2025-06-01T17:00:00Z",
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

@pytest.mark.django_db
def test_get_events_pagination():
    client = APIClient()

    category = EventCategory.objects.create(name="Music")
    venue = Venue.objects.create(name="Stadium", address="123 Street")
    organizer = Organizer.objects.create(name="EventCorp")

    for i in range(25):
        Event.objects.create(
            name=f"Event {i+1}",
            start_datetime=f"2025-05-{i+1:02d}T20:00:00Z",
            end_datetime=f"2025-05-{i+1:02d}T23:00:00Z",
            category=category,
            venue=venue,
            organizer=organizer,
        )

    url = reverse("event-list")
    response = client.get(url)

    assert response.status_code == 200
    assert response.data["count"] == 25
    assert len(response.data["results"]) == 10  

    url = reverse("event-list") + "?page=2"
    response = client.get(url)

    assert response.status_code == 200
    assert len(response.data["results"]) == 10  
    
    url = reverse("event-list") + "?page=3"
    response = client.get(url)

    assert response.status_code == 200
    assert len(response.data["results"]) == 5 