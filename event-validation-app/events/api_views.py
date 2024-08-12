from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from events.models import Event
from events.serializers import EventSerializer


# Create your views here.
class EventsListView(ReadOnlyModelViewSet):
    queryset = Event.objects.select_related("project", "major_tag", "minor_tag1", "minor_tag2")
    serializer_class = EventSerializer
    permission_classes = (IsAuthenticated, )
    pagination_class = None
    filter_backends = [OrderingFilter]
    ordering = ('id', )

    def list(self, request, *args, **kwargs):
        qs = self.filter_queryset(self.get_queryset())

        if query_params := request.query_params:

            if project_name := query_params.get("project_name"):
                qs = qs.filter(project__name=project_name)

            if start_datetime := query_params.get("start_datetime"):
                qs = qs.filter(datetime__gte=start_datetime)

            if end_datetime := query_params.get("end_datetime"):
                qs = qs.filter(datetime__lte=end_datetime)

        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)
