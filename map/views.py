import json, datetime

from django.shortcuts import get_object_or_404, render
from django.conf import settings
from django.views import View
from django.views.generic import ListView
from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from django.utils import timezone

from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.views import generic
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user
from django.core import serializers
from django.contrib.auth.decorators import user_passes_test

from .models import Event
from .forms import EventForm, EventFormSet


# Create your views here.

"""
Sources: 

Title: Using the Django authentication system
URL: https://docs.djangoproject.com/en/4.2/topics/auth/default/
Used to help ensure that the currently logged in user is an admin

Title: Dropdown select option to filter a Django list
URL: https://stackoverflow.com/questions/33726759/dropdown-select-option-to-filter-a-django-list
Used for reference when creating filters for event category for user convenience
"""


class MapView(View):
    template_name = "map/viewMap.html"
    key = settings.MAPS_KEY

    # def is_event_upcoming(self):
    #     return self.event_date_and_time >= timezone.now() and self.event_date_and_time <= timezone.now() + datetime.timedelta(days=1)

    def get(self, request):
        category_list = Event.objects.order_by('category').values_list('category', flat=True).distinct().filter(approved=True, event_date_and_time__gte=timezone.now()-datetime.timedelta(days=1))
        category_filter = request.GET.get('category_filter')
        # print(category_filter)
        
        # get approved events
        if category_filter is None or category_filter == "all":
            # approved_events = Event.objects.all().filter(approved=True)
            approved_events = Event.objects.all().filter(approved=True, event_date_and_time__gte=timezone.now()-datetime.timedelta(days=1))
        else:
            # approved_events = Event.objects.filter(approved=True, category=category_filter)
            approved_events = Event.objects.filter(approved=True, category=category_filter, event_date_and_time__gte=timezone.now()-datetime.timedelta(days=1))
        # print(len(approved_events))
        approved_events_json = serializers.serialize('json', approved_events)
        # print(approved_events_json)

        # get all events
        # events = Event.objects.all()
        all_data = {}
        # Populate the data dictionary with all of the events we need first
        for idx, event in enumerate(approved_events):
            all_data[idx] = {}

        # category = {}
        for idx, event in enumerate(approved_events):
            all_data[idx]["approved"] = event.approved
            all_data[idx]["category"] = event.category
            all_data[idx]["lat"] = f"{event.latitude}"
            all_data[idx]["lng"] = f"{event.longitude}"
            all_data[idx]["title"] = event.event_name
            
        # print(len(all_data))
        context = {
            "key": self.key,
            "data": json.dumps(all_data),
            "approved_events": approved_events_json,
            "categories": category_list,
            "events": Event.objects.all(),
            'user': request.user,
            'is_admin': is_admin(request.user),
        }
        return render(request, self.template_name, context)


class HomeView(View):
    template_name = "map/home.html"

    def get(self, request, *args, **kwargs):
        context = {
            'user': request.user,
            'is_admin': is_admin(request.user),
            'next': request.GET.get('next'),
        }
        return render(request, self.template_name, context)


def is_admin(user):
    return user.groups.filter(name='Admins').exists()



@user_passes_test(is_admin, login_url='/login/')
def unapproved_events(request):
    template_name = 'map/unapproved.html'
    queryset = Event.objects.filter(approved=False, deny_reason__isnull=True)

    # context_object_name = 'unapproved_events'

    context = {
        'user': request.user,
        'is_admin': is_admin(request.user),
        'unapproved_events': queryset,  # Pass the queryset directly
    }
    return render(request, template_name, context)


def approve_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    event.approved = True
    event.save()
    return redirect('unapproved-events')


def deny_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)

    if request.method == 'POST':
        deny_reason = request.POST.get('deny_reason')
        event.deny_reason = deny_reason
        event.approved = False  # Mark the event as denied
        event.save()

    return redirect('unapproved-events')


class CreateView(LoginRequiredMixin, generic.CreateView):
    form_class = EventForm
    template_name = "map/create.html"
    request = None

    # success_url = "home.html"
    # model = EventForm()

    def get(self, request, *args, **kwargs):
        # context = self.get_context_data(**kwargs)
        context = {}
        # context = super(CreateView, self).get(request)
        context['form'] = EventForm()
        context['event_formset'] = EventFormSet()
        context['key'] = settings.MAPS_KEY
        context['user'] = request.user
        context['is_admin'] = is_admin(request.user)
        
        return render(request, self.template_name, context)
    
    def get_context_data(self, request, **kwargs):
        context = super(CreateView, self).get_context_data(**kwargs)
        context['event_formset'] = EventFormSet()
        context['key'] = settings.MAPS_KEY
        context['user'] = request.user
        context['is_admin'] = is_admin(request.user)
        return context


    def post(self, request, *args, **kwargs):
        # print(self.request.POST)
        self.request = request
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        # print(request.POST)  # can see the actual returned data here
        event_formset = EventFormSet(self.request.POST, queryset=Event.objects.all())
        # print(form.is_valid() and event_formset.is_valid())

        if form.is_valid() and event_formset.is_valid():
            # print("Authenticated: ", request.user.is_authenticated)
            if request.user.is_authenticated:
                event = form.save(commit=False)
                # event.user = User.objects.get(username=request.user.username)  # Set the user to the currently logged-in user
                event.user = self.request.user
                event.save()
                return self.form_valid(form, event_formset)
            else:
                return self.form_invalid(request, form, event_formset)
        else:
            return self.form_invalid(request, form, event_formset)

    def get_queryset(self):
        return Event.objects.all()

    def form_valid(self, form, event_formset):
        self.object = form.save(commit=False)
        self.object.save()
        event_metas = event_formset.save(commit=False)
        for each in event_metas:
            self.object.save()
        return redirect(reverse("home"))

    def form_invalid(self, request, form, event_formset):
        # return self.render_to_response(self.get_context_data(request, form=form, event_formset=event_formset))
        return self.render_to_response(self.get_context_data(form=form, event_formset=event_formset, request=request))

@user_passes_test(is_admin, login_url='/login/')
def delete_event_view(request):
    template_name = 'map/deleteEvents.html'

    all_events = Event.objects.all()

    if request.method == 'POST':
        event_id = request.POST.get('event_id')
        if event_id:
            event = get_object_or_404(Event, pk=event_id)
            event.delete()
        return redirect('delete-event')

    context = {
        'user': request.user,
        'is_admin': is_admin(request.user),
        'all_events': all_events
    }
    return render(request, template_name, context)

def user_events(request):
    user_submitted_events = Event.objects.filter(user=request.user)
    context = {
        'user': request.user,
        'is_admin': is_admin(request.user),
        'user_submitted_events': user_submitted_events,
    }
    return render(request, 'map/userEvents.html', context)
