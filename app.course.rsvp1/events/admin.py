from django.contrib import admin
from .models import Event, RSVP


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("title", "speaker", "start_datetime", "end_datetime")
    search_fields = ("title", "speaker")
    list_filter = ("start_datetime",)


@admin.register(RSVP)
class RSVPAdmin(admin.ModelAdmin):
    list_display = ("event", "user", "full_name", "email", "created_at")
    search_fields = ("full_name", "email")
    list_filter = ("created_at",)


# Register your models here.
