import pytest
from django.core.exceptions import ObjectDoesNotExist
from events.models import Event, EventCategory, Organizer
from events.repositories import EventRepository


@pytest.mark.django_db
def test_get_all_events_success():
    category = EventCategory(name="Music")
    category.save()
    organizer = Organizer(name="BlackMusic")
    organizer.save()

    Event.objects.bulk_create(
        [
            Event(name="Evento 1", category=category, organizer=organizer),
            Event(name="Evento 2", category=category, organizer=organizer),
        ]
    )

    events = EventRepository.get_all_events()

    assert len(events) == 2


@pytest.mark.django_db
def test_get_event_by_id_success():
    category = EventCategory(name="Music")
    category.save()
    organizer = Organizer(name="BlackMusic")
    organizer.save()

    events = Event.objects.bulk_create(
        [
            Event(name="Evento 1", category=category, organizer=organizer),
            Event(name="Evento 2", category=category, organizer=organizer),
        ]
    )

    event_to_test = events[0]
    event = EventRepository.get_event_by_id(event_to_test.id)

    assert event.id == event_to_test.id


@pytest.mark.django_db
def test_get_event_by_id_wrong_id():
    category = EventCategory(name="Music")
    category.save()
    organizer = Organizer(name="BlackMusic")
    organizer.save()

    Event.objects.bulk_create(
        [
            Event(name="Evento 1", category=category, organizer=organizer),
            Event(name="Evento 2", category=category, organizer=organizer),
        ]
    )

    wrong_id = 99999

    event = EventRepository.get_event_by_id(wrong_id)

    assert event is None
