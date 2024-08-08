from django.urls import path

from events.views import EventsListView


urlpatterns = [
    path('api/events/', view=EventsListView.as_view({'get': 'list'}), name='events')
]
