from .models import Event
from typing import List


class EventRepository:
    @staticmethod
    def get_all_events() -> List[Event]:
        return Event.objects.all()

    @staticmethod
    def get_event_by_id(id: int) -> Event:
        try:
            return Event.objects.get(id=id)
        except Event.DoesNotExist:
            return None
