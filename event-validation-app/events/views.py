from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator

from django.views import View

from django.views.generic import ListView, DetailView
from django.utils import timezone
from django.utils.dateparse import parse_datetime

from events.models import Project, Event, Tag
from utils import EventStatus
from utils.functions import get_percentage_values


@method_decorator(login_required, name='dispatch')
class ProjectListView(ListView):
    template_name = 'project-list.html'
    model = Project
    context_object_name = 'projects'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context


class ProjectDetailView(DetailView):
    template_name = 'project-detail.html'
    model = Project
    context_object_name = 'project'
    queryset = Project.objects.prefetch_related('event_set')
    pk_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.get_object()
        qs = project.event_set

        if query_params := self.request.GET:

            if start_date := query_params.get('start_date'):
                start_date = timezone.make_aware(parse_datetime(start_date))
                qs = qs.filter(datetime__gte=start_date)

            if end_date := query_params.get('end_date'):
                end_date = timezone.make_aware(parse_datetime(end_date))
                qs = qs.filter(datetime__lte=end_date)

        totals = qs.totals_count()
        last_validated_event_datetime = qs.last_validated_event_datetime()

        totals = get_percentage_values(totals)
        context.update(**totals)
        context['last_validated_event_datetime'] = last_validated_event_datetime

        return context


class EventsValidationView(ListView):
    template_name = 'project-events.html'
    pk_url_kwarg = 'slug'
    context_object_name = "events"

    def get_queryset(self):
        project_id = self.kwargs.get('slug')
        qs = Event.objects.filter(project__slug=project_id)

        if query_params := self.request.GET:

            if start_date := query_params.get('start_date'):
                start_date = timezone.make_aware(parse_datetime(start_date))
                qs = qs.filter(datetime__gte=start_date)

            if end_date := query_params.get('end_date'):
                end_date = timezone.make_aware(parse_datetime(end_date))
                qs = qs.filter(datetime__lte=end_date)

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_choices'] = EventStatus.choices
        context['tags'] = Tag.objects.all()
        return context


class EventUpdateView(View):

    def post(self, request, *args, **kwargs):
        event_id = self.kwargs.get('pk')
        obj = get_object_or_404(Event, pk=event_id)
        field_name = request.POST.get('name')
        field_value = request.POST.get('value')

        if hasattr(obj, field_name):
            if field_name in ('major_tag', 'minor_tag1', 'minor_tag2'):
                tag = get_object_or_404(Tag, pk=field_value)
                field_value = tag

            setattr(obj, field_name, field_value)
            obj.save()
            return JsonResponse({'status': 'success'})
        return JsonResponse({'status': 'error'}, status=400)
