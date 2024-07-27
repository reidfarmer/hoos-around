# Create your models here.
from django.db import models
from users.models import User
from django.utils import timezone
import datetime

"""
Create your models here.
Sources for the model:

Title: Dropdown in Django Model
URL: https://stackoverflow.com/questions/31130706/dropdown-in-django-model
Used to add a dropdown when creating events to restrict possible event category choices


Title: Writing your first Django app, part 2
URL: https://docs.djangoproject.com/en/4.2/intro/tutorial02/
Used to change from regular datetime objects to timezone support for event occurrences
"""
class Event(models.Model):
    CATEGORY_CHOICES = (
        ('academic', 'ACADEMIC'),
        ('art', 'ART'),
        ('career', 'CAREER'),
        ('club', 'CLUB'),
        ('food', 'FOOD'),
        ('music', 'MUSIC'),
        ('social', 'SOCIAL'),
        ('sports', 'SPORTS'),
        ('volunteering', 'VOLUNTEERING'),
        ('other', 'OTHER'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event_name = models.CharField(max_length=100)
    event_description = models.CharField(max_length=500)
    location_name = models.CharField(max_length=100)
    event_address = models.CharField(max_length=200)
    event_date_and_time = models.DateTimeField(default=timezone.now)
    point_of_contact = models.CharField(max_length=50)
    latitude = models.CharField(max_length=50)
    longitude = models.CharField(max_length=50)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    requirements = models.CharField(max_length=500, default="")
    approved = models.BooleanField(default=False)
    deny_reason = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.event_name
    
    # def is_event_upcoming(self):
    #     return self.event_date_and_time >= timezone.now() and self.event_date_and_time <= timezone.now() + datetime.timedelta(days=1)
