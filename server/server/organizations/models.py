from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from server.schools.models import School
from server.users.models import User
from server.utils.model_fields import random_slug


class Organization(models.Model):
    slug = models.CharField(max_length=40, default=random_slug, unique=True)
    email = models.EmailField()
    description = models.CharField(max_length=250)
    website_url = models.URLField()
    name = models.CharField(max_length=50)
    goal = models.CharField(max_length=250)
    year_founded = models.CharField(max_length=4, null=True, blank=True)
    status = models.CharField(max_length=50)
    target_audience = models.JSONField()
    number_of_employees = models.PositiveIntegerField()
    number_of_members = models.PositiveIntegerField()
    number_of_volunteers = models.PositiveIntegerField()
    location_lon = models.DecimalField(max_digits=9, decimal_places=6)
    location_lat = models.DecimalField(max_digits=9, decimal_places=6)

    address_city = models.CharField(max_length=150)
    address_street = models.CharField(max_length=150)
    address_house_num = models.CharField(max_length=4)
    address_zipcode = models.CharField(max_length=9)
    cities = models.JSONField()
    districts = models.JSONField()
    union_type = models.CharField(max_length=50)


class Activity(models.Model):
    slug = models.CharField(max_length=40, default=random_slug, unique=True)
    name = models.CharField(max_length=35)
    target_audience = models.JSONField()
    domain = models.CharField(max_length=55)
    originization = models.ForeignKey(
        Organization, on_delete=models.SET_NULL, null=True, blank=True
    )
    description = models.CharField(max_length=400, default="")
    contact_name = models.CharField(max_length=60, default="")
    logo = models.ImageField(blank=True, null=True)
    phone_number = models.CharField(
        blank=True,
        max_length=15,
        validators=[
            RegexValidator(
                regex=r"^\d{9,15}$",
                message=_("phone number must be between 9-15 digits"),
            )
        ],
    )


class ActivityMedia(models.Model):
    slug = models.CharField(max_length=40, default=random_slug, unique=True)
    name = models.CharField(max_length=40)
    image_url = models.ImageField(blank=True, null=True)
    video_url = models.URLField(blank=True, null=True)
    activity = models.ForeignKey(
        Activity,
        on_delete=models.CASCADE,
        related_name="rich_media",
    )


class OrganizationMember(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="organization_member"
    )
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="organization_member",
    )


class SchoolActivityOrder(models.Model):
    class Meta:
        models.UniqueConstraint(fields=["school", "activity"], name="unique_order")

    class Status(models.TextChoices):
        PENDING_ADMIN_APPROVAL = "PENDING_ADMIN_APPROVAL", "Pending Admin Approval"
        APPROVED = "APPROVED", "Approved"

    base_status = Status.PENDING_ADMIN_APPROVAL

    requester = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="school_activity_orders",
    )
    school = models.ForeignKey(
        School, on_delete=models.CASCADE, related_name="school_activity_orders"
    )
    activity = models.ForeignKey(
        Activity, on_delete=models.CASCADE, related_name="school_activity_orders"
    )
    status = models.CharField(
        _("status"), max_length=50, choices=Status.choices, default=base_status
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
