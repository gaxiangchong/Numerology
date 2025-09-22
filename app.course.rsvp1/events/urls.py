from django.urls import path
from . import views


urlpatterns = [
    path("", views.EventListView.as_view(), name="list"),
    path("events/<int:pk>/", views.EventDetailView.as_view(), name="detail"),
    path("events/<int:pk>/rsvp/", views.EventRSVPView.as_view(), name="rsvp"),
]


