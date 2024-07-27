from map import views as view
from django.urls import path, include

urlpatterns = [
    path("", view.HomeView.as_view(), name="home"),
    path("map", view.MapView.as_view(), name="map"),
    path("createEvent", view.CreateView.as_view(), name="createEvent"),
    # path('unapproved-events/', view.UnapprovedEvents.as_view(), name='unapproved-events'),
    path('unapproved-events/', view.unapproved_events, name='unapproved-events'),
    path('approve-event/<int:event_id>/', view.approve_event, name='approve-event'),
    path('deny-event/<int:event_id>/', view.deny_event, name='deny-event'),
    path('delete-event/', view.delete_event_view, name='delete-event'),
    path('user-events/', view.user_events, name='user-events'),
]