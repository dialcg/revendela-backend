from django.urls import path
from .views import EventListAPIView

urlpatterns = [
    path('api/events/', EventListAPIView.as_view(), name='event-list'),
]