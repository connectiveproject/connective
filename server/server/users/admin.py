from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from server.users.forms import UserChangeForm
from server.users.helpers import send_user_invite

from .models import (
    Consumer,
    ConsumerProfile,
    Coordinator,
    CoordinatorProfile,
    Vendor,
    VendorProfile,
)

User = get_user_model()


def send_invite(self, request, queryset):
    for user in queryset:
        send_user_invite(user.email, request)


send_invite.short_description = "Invite user"


@admin.register(User, Coordinator, Consumer, Vendor)
class UserTypesAdmin(auth_admin.UserAdmin):
    form = UserChangeForm
    fieldsets = (
        (_("Account info"), {"fields": ("slug", "email", "password", "user_type")}),
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

    list_display = ["email", "slug"]
    search_fields = ["email"]
    actions = [send_invite]


admin.site.register(CoordinatorProfile)
admin.site.register(ConsumerProfile)
admin.site.register(VendorProfile)
