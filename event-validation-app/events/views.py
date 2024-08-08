from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ReadOnlyModelViewSet

from events.models import Event
from events.serializers import EventSerializer


# Create your views here.
class EventsListView(ReadOnlyModelViewSet):
    serializer_class = EventSerializer
    permission_classes = (AllowAny, )
    pagination_class = None

    def get_queryset(self):
        qs = Event.objects.select_related("project", "major_tag", "minor_tag1", "minor_tag2")
        return qs
