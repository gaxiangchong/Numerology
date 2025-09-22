from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import DetailView, ListView

from .forms import RSVPForm
from .models import Event, RSVP


class EventListView(ListView):
    model = Event
    template_name = "events/event_list.html"
    context_object_name = "events"


class EventDetailView(DetailView):
    model = Event
    template_name = "events/event_detail.html"
    context_object_name = "event"


class EventRSVPView(LoginRequiredMixin, View):
    def get(self, request: HttpRequest, pk: int) -> HttpResponse:
        event = get_object_or_404(Event, pk=pk)
        form = RSVPForm()
        return render(request, "events/event_rsvp.html", {"event": event, "form": form})

    def post(self, request: HttpRequest, pk: int) -> HttpResponse:
        event = get_object_or_404(Event, pk=pk)
        form = RSVPForm(request.POST)
        if form.is_valid():
            RSVP.objects.update_or_create(
                event=event,
                user=request.user,
                defaults={
                    "full_name": form.cleaned_data["full_name"],
                    "email": form.cleaned_data["email"],
                    "phone": form.cleaned_data.get("phone", ""),
                    "notes": form.cleaned_data.get("notes", ""),
                },
            )
            messages.success(request, "Your RSVP has been recorded.")
            return redirect(reverse("events:detail", args=[event.pk]))
        return render(request, "events/event_rsvp.html", {"event": event, "form": form})


# Create your views here.
