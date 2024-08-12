from django.urls import path

from events.api_views import EventsListView
from events.views import ProjectListView, ProjectDetailView


api_urlpatterns = [
    path('api/events/', view=EventsListView.as_view({'get': 'list'}), name='events')
]

template_urlpatterns = [
    path('projects/', view=ProjectListView.as_view(), name='project-list'),
    path('projects/<int:pk>/', view=ProjectDetailView.as_view(), name='project-detail')
]

urlpatterns = api_urlpatterns + template_urlpatterns
