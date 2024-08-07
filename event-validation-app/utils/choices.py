from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class EventStatus(TextChoices):
    TP = "TP", _("True Positive")
    TN = "TN", _("True Negative")
    FP = "FP", _("False Positive")
    FN = "FN", _("False Negative")


class BatchStatus(TextChoices):
    Preparation = "Preparation", _("Preparation")
    Ready = "Ready", _("Ready")
