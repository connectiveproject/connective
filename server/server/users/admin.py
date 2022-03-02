import logging

from django.conf import settings
from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from config import celery_app  # noqa TODO: check if necessary
from server.organizations.admin import OrganizationMemberTabularInline
from server.schools.admin import SchoolMemberTabularInline
from server.users.forms import UserChangeForm
from server.users.helpers import send_user_invite
from server.users.tasks import send_user_invite_task  # noqa TODO: check if necessary
from server.utils.logging.constants import INVITE_USER

from .models import (
    Consumer,
    ConsumerProfile,
    Coordinator,
    CoordinatorProfile,
    Instructor,
    InstructorProfile,
    Supervisor,
    SupervisorProfile,
    UserRole,
    Vendor,
    VendorProfile,
)

logger = logging.getLogger(__name__)
User = get_user_model()


def send_invite(self, request, queryset):
    for user in queryset:
        user_type = type(user).__name__
        user_id = user.id
        logger.info(f"{INVITE_USER} submit as task : {user_type} : {user.id}")
        send_user_invite_task.delay(user_id, user_type)


send_invite.short_description = "Invite user"


def send_invite_sync_deprecated(self, request, queryset):
    for user in queryset:
        send_user_invite(user)


send_invite_sync_deprecated.short_description = "Invite user (deprecated)"


@admin.register(User, Supervisor)
class BaseUserTypesAdmin(auth_admin.UserAdmin):
    form = UserChangeForm
    fieldsets = (
        (
            _("Account info"),
            {
                "fields": (
                    "slug",
                    "email",
                    "password",
                )
            },
        ),
        (_("Personal info"), {"fields": settings.ADMIN_USER_PERSONAL_INFO}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (None, {"classes": ("wide",), "fields": settings.ADMIN_ADD_USER_FIELDS}),
    )

    list_display = [
        "email",
        "slug",
        "date_joined",
        "is_signup_complete",
    ]
    search_fields = ["email"]
    actions = [send_invite, send_invite_sync_deprecated]


@admin.register(Coordinator, Consumer)
class SchoolUserTypesAdmin(BaseUserTypesAdmin):
    inlines = [SchoolMemberTabularInline]
    search_fields = ["email", "school_member__school__name"]


@admin.register(Instructor, Vendor)
class OrgUserTypesAdmin(BaseUserTypesAdmin):
    inlines = [OrganizationMemberTabularInline]


admin.site.register(CoordinatorProfile)
admin.site.register(ConsumerProfile)
admin.site.register(InstructorProfile)
admin.site.register(VendorProfile)
admin.site.register(SupervisorProfile)

admin.site.register(UserRole)
