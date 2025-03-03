from django.contrib import admin
from .models import EventCategory, Venue, Organizer, Event


@admin.register(EventCategory)
class EventCategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "address", "latitude", "longitude")
    search_fields = ("name", "address")
    list_filter = ("address",)


@admin.register(Organizer)
class OrganizerAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "start_datetime", "end_datetime", "venue", "category", "organizer")
    search_fields = ("name", "description")
    list_filter = ("start_datetime", "category", "organizer")
    ordering = ("-start_datetime",)
