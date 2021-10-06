from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from config import celery_app  # noqa TODO: check if necessary
from server.organizations.admin import OrganizationMemberTabularInline
from server.schools.admin import SchoolMemberTabularInline
from server.users.forms import UserChangeForm
from server.users.tasks import send_user_invite_task  # noqa TODO: check if necessary

from .models import (
    Consumer,
    ConsumerProfile,
    Coordinator,
    CoordinatorProfile,
    Instructor,
    InstructorProfile,
    Supervisor,
    SupervisorProfile,
    Vendor,
    VendorProfile,
)

User = get_user_model()


def send_invite(self, request, queryset):
    from datetime import datetime

    starttime = datetime.now()
    print(f"{starttime} starting...")
    for i in range(1, 1000):
        for user in queryset:
            send_user_invite_task.delay(user.email)
    duration = datetime.now() - starttime
    print(f"Ended in {duration}")


send_invite.short_description = "Invite user"


@admin.register(User, Supervisor)
class BaseUserTypesAdmin(auth_admin.UserAdmin):
    form = UserChangeForm
    fieldsets = (
        (_("Account info"), {"fields": ("slug", "email", "password")}),
        (_("Personal info"), {"fields": ("name",)}),
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
        (None, {"classes": ("wide",), "fields": ("email", "password1", "password2")}),
    )

    list_display = [
        "email",
        "slug",
        "date_joined",
    ]
    search_fields = ["email"]
    actions = [send_invite]


@admin.register(Coordinator, Consumer)
class SchoolUserTypesAdmin(BaseUserTypesAdmin):
    inlines = [SchoolMemberTabularInline]


@admin.register(Instructor, Vendor)
class OrgUserTypesAdmin(BaseUserTypesAdmin):
    inlines = [OrganizationMemberTabularInline]


admin.site.register(CoordinatorProfile)
admin.site.register(ConsumerProfile)
admin.site.register(InstructorProfile)
admin.site.register(VendorProfile)
admin.site.register(SupervisorProfile)
