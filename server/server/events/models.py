from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from server.organizations.models import SchoolActivityGroup
from server.schools.models import School
from server.users.models import Consumer, Instructor, User
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
    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        related_name="school_event_orders",
        blank=True,
        null=True,
    )
    title = models.CharField(max_length=250, null=True, blank=True)
    filter_genders = models.JSONField(null=True, blank=True)
    filter_grades = models.JSONField(null=True, blank=True)

    instructor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="instructor_event_orders",
    )
    additional_instructors = models.ManyToManyField(
        User,
        related_name="additional_instructor_event_orders",
        blank=True,
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
        has_consumer_filters = self.filter_genders and self.filter_grades
        if not has_consumer_filters and (self.filter_genders or self.filter_genders):
            raise ValidationError(
                {
                    "filter_genders": "filter_genders and filter_grades must be set or empty together"
                }
            )
        if (has_consumer_filters and self.school_group) or (
            not has_consumer_filters and not self.school_group
        ):
            raise ValidationError("one of school_group or filter_* fields must be set")


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
    title = models.CharField(max_length=250, null=True, blank=True)
    filter_genders = models.JSONField(null=True, blank=True)
    filter_grades = models.JSONField(null=True, blank=True)
    instructor = models.ForeignKey(
        Instructor,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="instructor_events",
    )
    additional_instructors = models.ManyToManyField(
        User,
        related_name="additional_instructor_events",
        blank=True,
    )
    consumers = models.ManyToManyField(
        "users.Consumer",
        blank=True,
    )
    ext_consumers_attended = summary_general_rating = models.IntegerField(
        validators=[MinValueValidator(1)],
        null=True,
        blank=True,
    )
    school_group = models.ForeignKey(
        SchoolActivityGroup,
        on_delete=models.SET_NULL,
        blank=True,
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

    # date/time when the event summarized or marked as canceled by the instructor
    summary_time = models.DateTimeField(null=True, blank=True)

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
        group = self.school_group
        if not group:
            group = f"FILTER: {self.filter_genders} | {self.filter_grades}"
        return f"{group} : {self.start_time} : {self.slug}"

    def save(self, *args, **kwargs):
        if (self.has_summary or self.is_canceled) and self.summary_time is None:
            self.summary_time = timezone.now()
        super().save(*args, **kwargs)

    def group_display_name(self):
        """
        This returns the display name of the group. For real groups, it is the
        name of the group. For "filter groups", it is description of the filters.
        NOTE: for real group this method may do a database query - don't use in loops
        without select_related() before
        """
        if self.school_group:
            return self.school_group.name
        all_genders: bool = len(self.filter_genders) >= 2
        all_grades: bool = len(self.filter_grades) >= 12
        if all_genders and all_grades:
            return _("event.group_name.all.all")
        if all_grades:
            return _(f"event.group_name.all.{self.filter_genders[0].lower()}")
        grades = ", ".join(
            [_(f"grades.{grade}").__str__() for grade in self.filter_grades]
        )
        if all_genders:
            return f"{_('event.group_name.grades')} {grades}"
        gender = _(f"event.group_name.gender.{self.filter_genders[0].lower()}")
        return f"{_('event.group_name.grades')} {grades} {gender}"

    def get_consumers_filter_queryset(self):
        return Consumer.objects.filter(
            consumerprofile__gender__in=self.filter_genders,
            consumerprofile__grade__in=self.filter_grades,
            school_member__school=self.event_order.school,
        )


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
