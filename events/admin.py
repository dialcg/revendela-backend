from django.contrib import admin
from .models import Event, EventCategory, Organizer, Venue

admin.site.register(Event)
admin.site.register(EventCategory)
admin.site.register(Organizer)
admin.site.register(Venue)
