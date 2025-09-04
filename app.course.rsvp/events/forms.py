from django import forms
from .models import RSVP


class RSVPForm(forms.ModelForm):
    remember_me = forms.BooleanField(required=False, initial=True)

    class Meta:
        model = RSVP
        fields = ["full_name", "email", "phone", "notes"]


