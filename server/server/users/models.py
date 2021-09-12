from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import RegexValidator
from django.db import models
from django.db.models import (
    BooleanField,
    CharField,
    DateTimeField,
    EmailField,
    TextChoices,
)
from django.db.models.base import ModelBase
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from server.utils.model_fields import random_slug


class UserRegistrator(ModelBase):
    def __new__(cls, name, bases, attrs):
        """
        add all user types to enum and set base user type for each subclass
        """
        if name == "User":
            return super().__new__(cls, name, bases, attrs)

        all_types = [t.name for t in bases[0].Types] + [name.upper()]
        bases[0].Types = TextChoices("Types", " ".join(all_types))
        newcls = super().__new__(cls, name, bases, attrs)
        newcls.base_user_type = name.upper()
        return newcls


class User(AbstractUser, metaclass=UserRegistrator):
    """Default user for server."""

    Types = models.TextChoices("Types", "USER")
    base_user_type = Types.USER

    user_type = CharField(
        _("Type"), max_length=50, choices=Types.choices, default=base_user_type
    )

    #: First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore
    last_name = None  # type: ignore

    email = EmailField(unique=True)
    username = CharField(max_length=40, default=random_slug, unique=True)
    slug = CharField(max_length=40, default=random_slug, unique=True)
    is_signup_complete = BooleanField(default=False)
    terms_of_use_acceptance_date = DateTimeField(null=True, blank=True)

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})

    def save(self, *args, **kwargs):
        if not self.id:
            self.user_type = self.base_user_type
            self.slug = self.username

        self.email = self.email.lower()
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.email


class ConsumerManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        return (
            super()
            .get_queryset(*args, **kwargs)
            .filter(
                user_type="CONSUMER",
            )
        )


class CoordinatorManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        return (
            super()
            .get_queryset(*args, **kwargs)
            .filter(
                user_type="COORDINATOR",
            )
        )


class SupervisorManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        return (
            super()
            .get_queryset(*args, **kwargs)
            .filter(
                user_type="SUPERVISOR",
            )
        )


class VendorManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        return (
            super()
            .get_queryset(*args, **kwargs)
            .filter(
                user_type="VENDOR",
            )
        )


class InstructorManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        return (
            super()
            .get_queryset(*args, **kwargs)
            .filter(
                user_type="INSTRUCTOR",
            )
        )


class Consumer(User):
    base_user_type = None
    objects = ConsumerManager()

    class Meta:
        proxy = True
        verbose_name_plural = "1. Consumer (Students)"

    @property
    def profile(self):
        return self.consumerprofile


class Coordinator(User):
    base_user_type = None
    objects = CoordinatorManager()

    class Meta:
        proxy = True
        verbose_name_plural = "2. Coordinator (Principals)"

    @property
    def profile(self):
        return self.coordinatorprofile


class Vendor(User):
    base_user_type = None
    objects = VendorManager()

    class Meta:
        proxy = True
        verbose_name_plural = "3. Vendor (Organization Managers)"

    @property
    def profile(self):
        return self.vendorprofile


class Instructor(User):
    base_user_type = None
    objects = InstructorManager()

    class Meta:
        proxy = True
        verbose_name_plural = "4. Instructor (Guide)"

    @property
    def profile(self):
        return self.instructorprofile


class Supervisor(User):
    base_user_type = None
    objects = SupervisorManager()

    class Meta:
        proxy = True
        verbose_name_plural = "5. Supervisor"

    @property
    def profile(self):
        return self.supervisorprofile


class BaseProfile(models.Model):
    class Gender(TextChoices):
        MALE = "MALE", "Male"
        FEMALE = "FEMALE", "Female"
        OTHER = (
            "OTHER",
            "Other",
        )
        UNKNOWN = "UNKNOWN", "Unknown"

    base_gender = Gender.UNKNOWN

    user = models.OneToOneField(
        User, related_name="%(class)s", on_delete=models.CASCADE, unique=True
    )
    gender = models.CharField(
        _("Gender"), max_length=50, choices=Gender.choices, default=base_gender
    )
    profile_picture = models.JSONField(blank=True, null=True, default=dict)

    class Meta:
        abstract = True

    def __str__(self):
        return f"PROFILE | {self.user.user_type} | {self.user.email}"


class CoordinatorProfile(BaseProfile):
    job_description = models.CharField(max_length=50, default="")
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


class SupervisorProfile(BaseProfile):
    job_description = models.CharField(max_length=50, default="")
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


class ConsumerProfile(BaseProfile):
    pass


class VendorProfile(BaseProfile):
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


class InstructorProfile(BaseProfile):
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
