from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils.text import slugify

from events.querysets import EventsQuerySet
from utils import EventStatus, BatchStatus
from utils.models import TimeStampedModel, SoftDeletableModel


# Create your models here.
class Project(TimeStampedModel, SoftDeletableModel):
    slug = models.CharField(primary_key=True, unique=True)
    name = models.CharField(max_length=200)
    validation_guide_link = models.CharField(max_length=200)

    def get_validation_page_url(self):
        return reverse('project-events', kwargs={'slug': self.pk})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Project, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Tag(TimeStampedModel, SoftDeletableModel):
    name = models.CharField(max_length=200)
    project = models.ForeignKey(Project, to_field='slug', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name


class Event(TimeStampedModel, SoftDeletableModel):
    datetime = models.DateTimeField(blank=True, null=True)
    link = models.CharField(max_length=200)
    uid = models.CharField(max_length=200)
    portal_comment = models.CharField(max_length=2000, null=True, blank=True)
    internal_comment = models.CharField(max_length=2000, null=True, blank=True)
    taken_for_annotation = models.BooleanField(default=False, help_text="Events taken for annotation should not be used for model evaluation")
    cam_uid = models.CharField(max_length=200, help_text="The camera uid from which the event was captured from", null=True, blank=True)
    validated = models.BooleanField(default=False)
    portal_status = models.CharField(max_length=200, choices=EventStatus.choices, null=True, blank=True)
    internal_status = models.CharField(max_length=200, choices=EventStatus.choices, null=True, blank=True)
    # Foreign fields
    project = models.ForeignKey(Project, to_field='slug', on_delete=models.SET_NULL, null=True, blank=True)
    major_tag = models.ForeignKey(Tag, on_delete=models.SET_NULL, null=True, blank=True, related_name="major_tag_set")
    minor_tag1 = models.ForeignKey(Tag, on_delete=models.SET_NULL, null=True, blank=True, related_name="minor_tag1_set")
    minor_tag2 = models.ForeignKey(Tag, on_delete=models.SET_NULL, null=True, blank=True, related_name="minor_tag2_set")

    objects = EventsQuerySet.as_manager()


class EventDownloadBatch(TimeStampedModel, SoftDeletableModel):
    """Downloadable archive with events"""
    requester = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, help_text="User who requested to download a batch of events")
    status = models.CharField(max_length=200, choices=BatchStatus.choices)
    link = models.CharField(max_length=400)
