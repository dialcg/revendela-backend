from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from .repositories import EventRepository
from .serializers import EventSerializer
from rest_framework.filters import SearchFilter, OrderingFilter

class EventListAPIView(generics.ListAPIView):
    serializer_class = EventSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name', 'description', 'category__name', 'organizer__name']
    ordering_fields = ['name', 'date']
    pagination_class = PageNumberPagination

    def get_queryset(self):
        return EventRepository.get_all_events()