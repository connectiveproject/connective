from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from server.organizations.models import SchoolActivityGroup
from server.utils.db_utils import get_base_model
from server.utils.model_fields import random_slug


class EventOrder(get_base_model()):
    class Status(models.TextChoices):
        CANCELLED = "CANCELLED", "Cancelled"
        PENDING_APPROVAL = "PENDING_APPROVAL", "Pending Approval"
        APPROVED = "APPROVED", "Approved"
        DENIED = "DENIED", "Denied"

    class Recurrence(models.TextChoices):
        ONE_TIME = "ONE_TIME", "One Time"
        WEEKLY = "WEEKLY", "Weekly"

    base_status = Status.PENDING_APPROVAL
    base_recurrence = Recurrence.ONE_TIME

    slug = models.CharField(max_length=40, default=random_slug, unique=True)
    status = models.CharField(
        _("status"), max_length=50, choices=Status.choices, default=base_status
    )
    recurrence = models.CharField(
        _("recurrence"),
        max_length=50,
        choices=Recurrence.choices,
        default=base_recurrence,
    )
    school_group = models.ForeignKey(
        SchoolActivityGroup,
        on_delete=models.CASCADE,
        null=True,
    )
    locations_name = models.CharField(
        max_length=250,
        null=True,
        blank=True,
    )
    status_reason = models.CharField(
        max_length=250,
        blank=True,
    )
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.start_time > self.end_time:
            raise ValidationError(
                {"end_time": _("end time must occur after start time")}
            )


class Event(get_base_model()):
    class CancellationReasons(models.TextChoices):
        ILLNESS = "ILLNESS", _("Illness")
        WEATHER = "WEATHER", _("Weather")
        EXAM_SEASON = "EXAM_SEASON", _("Exam Season")
        COVID_19 = "COVID_19", _("COVID-19")
        HOLIDAY = "HOLIDAY", _("Holiday")
        OTHER = "OTHER", _("Other")

    slug = models.CharField(max_length=40, default=random_slug, unique=True)
    event_order = models.ForeignKey(
        EventOrder, on_delete=models.CASCADE, null=True, related_name="events"
    )
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    consumers = models.ManyToManyField(
        "users.Consumer",
        blank=True,
    )
    school_group = models.ForeignKey(
        SchoolActivityGroup,
        on_delete=models.SET_NULL,
        null=True,
    )
    locations_name = models.CharField(
        max_length=250,
        null=True,
        blank=True,
    )
    has_summary = models.BooleanField(default=False)
    summary_general_notes = models.CharField(
        max_length=400,
        null=True,
        blank=True,
    )
    summary_general_rating = models.IntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(10),
        ],
        null=True,
        blank=True,
    )
    summary_children_behavior = models.IntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(10),
        ],
        null=True,
        blank=True,
    )
    is_canceled = models.BooleanField(default=False)
    cancellation_reason = models.CharField(
        max_length=200, choices=CancellationReasons.choices, blank=True
    )

    def clean(self):
        if self.start_time > self.end_time:
            raise ValidationError(
                {"end_time": _("end time must occur after start time")}
            )

    def __str__(self):
        return f"{self.school_group} : {self.start_time} : {self.slug}"


class ConsumerEventFeedback(get_base_model()):
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["consumer", "event"], name="unique consumer feedback"
            )
        ]

    slug = models.CharField(max_length=40, default=random_slug, unique=True)
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
    )
    consumer = models.ForeignKey(
        "users.Consumer",
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
    )
    general_notes = models.CharField(
        max_length=400,
        blank=True,
    )
    secondary_notes = models.CharField(
        max_length=400,
        blank=True,
    )
    general_rating = models.IntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(10),
        ],
        null=True,
        blank=True,
    )
    secondary_rating = models.IntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(10),
        ],
        null=True,
        blank=True,
    )
