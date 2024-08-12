from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView

from events.models import Project


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
    pk_url_kwarg = 'pk'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project_id = self.kwargs.get('pk')

        project = get_object_or_404(Project, id=project_id)
        context['project'] = project

        qs = project.event_set

        if query_params := self.request.GET:

            if start_date := query_params.get('start_date'):
                qs = qs.filter(datetime__gte=start_date)

            if end_date := query_params.get('end_date'):
                qs = qs.filter(datetime__lte=end_date)

        totals = qs.totals_count()
        last_validated_event_datetime = qs.last_validated_event_datetime()

        context.update(**totals)
        context['last_validated_event_datetime'] = last_validated_event_datetime
        print(context)
        return context
