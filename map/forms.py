from django import forms
from django.forms import inlineformset_factory
from .models import Event
from users.models import User
"""
Sources for the event creation form:
Title: How to customize Date and Time field in django forms?
URL: https://stackoverflow.com/questions/74109872/how-to-customize-date-and-time-field-in-django-forms
Used to restrict events to only have valid dates and times entered instead of just plain string input
"""
class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['event_name', 'event_description', 'location_name', 'event_address',
                  'event_date_and_time', 'point_of_contact', 'category', "latitude", "longitude",
                  'requirements']
        widgets = {
            'latitude': forms.HiddenInput(), 
            "longitude": forms.HiddenInput(),
            "event_date_and_time": forms.TextInput(attrs={'type': 'datetime-local'}),
        }  # this needs to be widgets (with the s)


EventFormSet = inlineformset_factory(
    User,
    Event,
    EventForm,
    extra=1,
    can_delete=False
)
