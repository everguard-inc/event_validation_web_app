from django.db import models
from django.db.models import Count, Q

from utils import EventStatus


class EventsQuerySet(models.QuerySet):

    def totals_count(self):

        aggregation = self.aggregate(
            total=Count('id'),
            # Internal wise
            fp_count_internal=Count('id', filter=Q(internal_status=EventStatus.FP)),
            fn_count_internal=Count('id', filter=Q(internal_status=EventStatus.FN)),
            tp_count_internal=Count('id', filter=Q(internal_status=EventStatus.TP)),
            tn_count_internal=Count('id', filter=Q(internal_status=EventStatus.TN)),
            # Portal wise
            fp_count_portal=Count('id', filter=Q(portal_status=EventStatus.FP)),
            fn_count_portal=Count('id', filter=Q(portal_status=EventStatus.FN)),
            tp_count_portal=Count('id', filter=Q(portal_status=EventStatus.TP)),
            tn_count_portal=Count('id', filter=Q(portal_status=EventStatus.TN)),

            not_validated=Count('id', filter=Q(validated=False)),
        )
        return aggregation

    def last_validated_event_datetime(self):
        last_validated_event = self.filter(validated=True).order_by('-datetime').first()
        return last_validated_event.datetime if last_validated_event else None
