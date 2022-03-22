import logging
from typing import Dict, List

from django.contrib.auth import get_user_model
from django.contrib.auth.models import BaseUserManager
from django.core.validators import RegexValidator
from django.db import models
from django.db.models import BooleanField, CharField, EmailField, TextChoices
from django.db.models.base import ModelBase
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from server.utils.db_utils import get_base_abstract_user_model, get_base_model
from server.utils.model_fields import random_slug
from server.utils.privileges import ROLES

logger = logging.getLogger(__name__)


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


class RoleScope:
    def __init__(self):
        self.roles = []
        self.admin_scope = False

    def update(self, role):
        self.roles.append(role)
        if role.admin_scope:
            self.admin_scope = True

    def is_admin_scope(self) -> bool:
        return self.admin_scope

    def get_schools(self) -> List:
        result = []
        for user_role in self.roles:
            result.append(user_role.school)
        return result

    def get_organizations(self) -> List:
        result: List = []
        user_role: UserRole
        for user_role in self.roles:
            result.append(user_role.organization)
        return result


class User(get_base_abstract_user_model(), metaclass=UserRegistrator):
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

    def calculate_privilege_scopes(self) -> Dict[str, RoleScope]:
        result: Dict[str, RoleScope] = {}
        roles = self.roles.all()
        for user_role in roles:
            if user_role.role_code not in ROLES:
                logger.warning(f"Unknown role: {user_role.role_code}")
                continue
            user_privileges = ROLES[user_role.role_code]
            for privilege in user_privileges:
                scope: RoleScope = result.get(privilege, RoleScope())
                scope.update(user_role)
                result[privilege] = scope
        return result

    def get_privilege_scopes(self) -> Dict[str, RoleScope]:
        if not hasattr(self, "get_privilege_scopes_dict"):
            self.get_privilege_scopes_dict = self.calculate_privilege_scopes()
        return self.get_privilege_scopes_dict

    def __str__(self):
        return self.email


class UserRole(get_base_model()):

    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="roles",
        verbose_name=_("User"),
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    role_code = CharField(max_length=50, null=False, blank=False)

    admin_scope = BooleanField(
        default=False
    )  # when true, scope of this role is all schools/organizations

    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.CASCADE,
        related_name="roles",
        verbose_name="Organization",
        null=True,
        blank=True,
    )

    school = models.ForeignKey(
        "schools.School",
        on_delete=models.CASCADE,
        related_name="roles",
        verbose_name="School",
        null=True,
        blank=True,
    )

    class Meta:
        unique_together = ("user", "role_code", "school_id", "organization_id")
        verbose_name = _("User Role")
        verbose_name_plural = _("User Roles")

    def __str__(self):
        return f"{self.role_code}"


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


class BaseProfile(get_base_model()):
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
    invitation_count = models.PositiveIntegerField(default=0)
    last_invite_sent = models.DateTimeField(
        auto_now=False, auto_now_add=False, null=True, blank=True
    )

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

    class Meta:
        abstract = True

    def __str__(self):
        return f"PROFILE | {self.user.user_type} | {self.user.email}"


class CoordinatorProfile(BaseProfile):
    job_description = models.CharField(max_length=50, default="")


class SupervisorProfile(BaseProfile):
    job_description = models.CharField(max_length=50, default="")


class ConsumerProfile(BaseProfile):
    pass


class VendorProfile(BaseProfile):
    pass


class InstructorProfile(BaseProfile):
    pass


USER_TYPE_TO_MODEL = {
    "Consumer": Consumer,
    "Coordinator": Coordinator,
    "Instructor": Instructor,
    "Supervisor": Supervisor,
    "Vendor": Vendor,
}


class NotificationManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()


class Notification(get_base_model()):

    objects = NotificationManager()

    class Status(models.TextChoices):
        NEW = "NEW", "New"
        READ = "READ", "Read"
        DISMISSED = "DISMISSED", "Dismissed"

    slug = CharField(max_length=40, default=random_slug, unique=True)

    created_at = models.DateTimeField(auto_now_add=True)

    notification_code = models.CharField(max_length=100, null=False, blank=False)

    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="notifications",
    )

    parameters = models.JSONField(max_length=500, null=True, blank=True)

    status = models.CharField(
        max_length=50,
        choices=Status.choices,
        default=Status.NEW,
    )


class UserUtil:
    def __init__(self):
        self.user_type_to_profile: Dict[str, BaseProfile] = {
            "CONSUMER": ConsumerProfile,
            "COORDINATOR": CoordinatorProfile,
            "INSTRUCTOR": InstructorProfile,
            "SUPERVISOR": SupervisorProfile,
            "VENDOR": VendorProfile,
        }

    def get_profile_class(self, user_type: str):
        return self.user_type_to_profile[user_type]

    def get_user_profile(self, user: User) -> BaseProfile:
        profile_class = self.get_profile_class(user.user_type)
        return profile_class.objects.get(user=user)
