from django.urls import path

from events.api_views import EventsListView
from events.views import ProjectListView, ProjectDetailView, EventsValidationView, EventUpdateView


api_urlpatterns = [
    path('api/events/', view=EventsListView.as_view({'get': 'list'}), name='api-events')
]

template_urlpatterns = [
    path('projects/', view=ProjectListView.as_view(), name='project-list'),
    path('projects/<str:slug>/', view=ProjectDetailView.as_view(), name='project-detail'),
    path('projects/<str:slug>/validation/', view=EventsValidationView.as_view(), name='project-events'),
    path('events/<int:pk>/update/', view=EventUpdateView.as_view(), name='event-update')
]

urlpatterns = api_urlpatterns + template_urlpatterns
