from django.db import models
from django.conf import settings
from utils import EventStatus, BatchStatus


# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length=200)
    validation_guide_link = models.CharField(max_length=200)


class Tag(models.Model):
    name = models.CharField(max_length=200)
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, blank=True)


class Event(models.Model):
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
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, blank=True)
    major_tag = models.ForeignKey(Tag, on_delete=models.SET_NULL, null=True, blank=True, related_name="major_tag_set")
    minor_tag1 = models.ForeignKey(Tag, on_delete=models.SET_NULL, null=True, blank=True, related_name="minor_tag1_set")
    minor_tag2 = models.ForeignKey(Tag, on_delete=models.SET_NULL, null=True, blank=True, related_name="minor_tag2_set")


class EventDownloadBatch(models.Model):
    """Downloadable archive with events"""
    requester = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, help_text="User who requested to download a batch of events")
    status = models.CharField(max_length=200, choices=BatchStatus.choices)
    link = models.CharField(max_length=400)