from rest_framework import serializers
from .models import Event

class EventSerializer(serializers.ModelSerializer):
    latitude = serializers.CharField(source="venue.latitude", read_only=True)
    longitude = serializers.CharField(source="venue.longitude", read_only=True)

    class Meta:
        model = Event
        fields = [
            "id", "name", "description", "start_datetime", "end_datetime",
            "venue", "category", "image", "organizer", "latitude", "longitude"
        ]