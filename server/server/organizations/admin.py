import analytics
from django.contrib import admin

from server.utils.analytics_utils.constants import (
    EVENT_ACTIVITY_CREATED,
    EVENT_ACTIVITY_GROUP_CREATED,
    EVENT_ACTIVITY_ORDER_STATUS_UPDATED,
)
from server.utils.analytics_utils.decorators import (
    track_admin_create,
    track_admin_field_update,
)

from .models import (
    Activity,
    ActivityMedia,
    ImportedActivity,
    ImportedOrganization,
    Organization,
    OrganizationMember,
    SchoolActivityGroup,
    SchoolActivityOrder,
)


def approve_order(self, request, queryset):
    for order in queryset:
        if order.status == SchoolActivityOrder.Status.APPROVED:
            continue

        order.status = SchoolActivityOrder.Status.APPROVED
        order.save()
        analytics.track(
            request.user.slug,
            EVENT_ACTIVITY_ORDER_STATUS_UPDATED,
            {
                "slug": order.slug,
                "activity_slug": order.activity.slug,
                "school_slug": order.school.slug,
                "status": order.status,
            },
        )


approve_order.short_description = "Approve Selected Orders"


class OrganizationMemberTabularInline(admin.TabularInline):
    model = OrganizationMember
    min_num = 1


@admin.register(SchoolActivityOrder)
class SchoolActivityOrderAdmin(admin.ModelAdmin):
    list_display = ["school", "activity", "created_at", "updated_at", "status"]
    search_fields = ["school__name", "activity__name"]
    list_filter = ["status"]
    actions = [approve_order]

    @track_admin_field_update(
        EVENT_ACTIVITY_ORDER_STATUS_UPDATED,
        ["slug", "activity__slug", "school__slug", "status"],
        field_to_track="status",
        fields_rename={
            "activity__slug": "activity_slug",
            "school__slug": "school_slug",
        },
    )
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ["slug", "name", "originization", "tags"]
    search_fields = ["name"]

    @track_admin_create(EVENT_ACTIVITY_CREATED, ["slug", "name", "domain"])
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)


@admin.register(SchoolActivityGroup)
class SchoolActivityGroupAdmin(admin.ModelAdmin):
    list_display = [
        "slug",
        "name",
        "school",
        "activity",
        "group_type",
        "instructor",
        "activity_order",
    ]
    list_filter = ["group_type"]
    search_fields = ["name"]

    def school(self, obj):
        return obj.activity_order.school

    def activity(self, obj):
        return obj.activity_order.activity

    @track_admin_create(
        EVENT_ACTIVITY_GROUP_CREATED,
        ["slug", "name", "group_type", "activity_order__slug"],
        fields_rename={"activity_order__slug": "activity_order_slug"},
    )
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)


admin.site.register(Organization)
admin.site.register(ActivityMedia)
admin.site.register(OrganizationMember)
admin.site.register(ImportedOrganization)
admin.site.register(ImportedActivity)
