from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from taggit.managers import TaggableManager

from server.schools.models import School
from server.users.models import Consumer, Instructor, User
from server.utils.model_fields import random_slug


class SchoolActivityGroupManager(models.Manager):
    def get_sibling_container_only_group(self, activity_group):
        container_only_groups = self.filter(
            activity_order=activity_group.activity_order,
            group_type=SchoolActivityGroup.GroupTypes.CONTAINER_ONLY,
        )
        if container_only_groups.exists():
            return container_only_groups[0]

        return None


class Organization(models.Model):
    slug = models.CharField(max_length=40, default=random_slug, unique=True)
    organization_number = models.CharField(max_length=10, unique=True, null=True)
    email = models.EmailField()
    description = models.CharField(max_length=250)
    website_url = models.URLField(null=True, blank=True)
    name = models.CharField(max_length=50)
    goal = models.CharField(max_length=250, null=True, blank=True)
    year_founded = models.CharField(max_length=4, null=True, blank=True)
    status = models.CharField(max_length=50, null=True, blank=True)
    target_audience = models.JSONField(null=True, blank=True)
    number_of_employees = models.PositiveIntegerField(null=True, blank=True)
    number_of_members = models.PositiveIntegerField(null=True, blank=True)
    number_of_volunteers = models.PositiveIntegerField(null=True, blank=True)
    location_lon = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
    )
    location_lat = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
    )

    address_city = models.CharField(max_length=150, null=True, blank=True)
    address_street = models.CharField(max_length=150, null=True, blank=True)
    address_house_num = models.CharField(max_length=4, null=True, blank=True)
    address_zipcode = models.CharField(max_length=9, null=True, blank=True)
    cities = models.JSONField(null=True, blank=True)
    districts = models.JSONField(null=True, blank=True)
    union_type = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"{self.name} | {self.slug}"


class Activity(models.Model):
    tags = TaggableManager()

    slug = models.CharField(max_length=40, default=random_slug, unique=True)
    name = models.CharField(max_length=35)
    target_audience = models.JSONField()
    domain = models.CharField(max_length=55, null=True, blank=True)
    originization = models.ForeignKey(
        Organization, on_delete=models.SET_NULL, null=True, blank=True
    )
    activity_website_url = models.URLField(null=True, blank=True)
    activity_email = models.EmailField(null=True, blank=True)
    description = models.CharField(max_length=550, default="")
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

    def __str__(self):
        try:
            return f"{self.name} | {self.slug} | {self.originization.name}"
        except AttributeError:
            return f"{self.name} | {self.slug}"


class ActivityMedia(models.Model):
    slug = models.CharField(max_length=40, default=random_slug, unique=True)
    name = models.CharField(max_length=40, null=True, blank=True)
    image_url = models.ImageField(blank=True, null=True)
    video_url = models.URLField(blank=True, null=True)
    activity = models.ForeignKey(
        Activity,
        on_delete=models.CASCADE,
        related_name="rich_media",
    )

    def __str__(self):
        return f"{self.name} | {self.slug} | {self.activity.name}"


class OrganizationMember(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="organization_member"
    )
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="organization_member",
    )

    def __str__(self):
        return f"{self.user.email} | {self.organization.name}"


class SchoolActivityOrder(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["school", "activity"], name="unique_order")
        ]

    class Status(models.TextChoices):
        CANCELLED = "CANCELLED", "Cancelled"
        PENDING_ADMIN_APPROVAL = "PENDING_ADMIN_APPROVAL", "Pending Admin Approval"
        APPROVED = "APPROVED", "Approved"

    base_status = Status.PENDING_ADMIN_APPROVAL

    slug = models.CharField(max_length=40, default=random_slug, unique=True)
    requested_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="requested_orders",
    )
    last_updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="last_updated_by_me_orders",
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

    def __str__(self):
        return f"{self.activity} | {self.school} | {self.status} | {self.pk}"


class SchoolActivityGroup(models.Model):
    class GroupTypes(models.TextChoices):
        CONTAINER_ONLY = "CONTAINER_ONLY", "Container Only"
        DISABLED_CONSUMERS = "DISABLED_CONSUMERS", "Disabled Consumers"
        DEFAULT = "DEFAULT", "Default"

    objects = SchoolActivityGroupManager()

    slug = models.CharField(max_length=40, default=random_slug, unique=True)
    activity_order = models.ForeignKey(
        SchoolActivityOrder, on_delete=models.CASCADE, related_name="activity_groups"
    )
    name = models.CharField(_("name"), max_length=50)
    description = models.CharField(_("description"), max_length=550)
    consumers = models.ManyToManyField(
        Consumer,
        related_name="activity_groups",
        blank=True,
    )
    group_type = models.CharField(
        _("group type"),
        max_length=50,
        choices=GroupTypes.choices,
        default=GroupTypes.DEFAULT,
    )
    instructor = models.ForeignKey(
        Instructor,
        on_delete=models.SET_NULL,
        related_name="managed_activity_groups",
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.name} : {self.group_type} : {self.slug} : \
        {self.activity_order.activity.name} : {self.activity_order.school.name}"
