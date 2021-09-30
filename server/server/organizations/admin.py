import analytics
from django.contrib import admin

from server.utils.analytics_utils.constants import (
    EVENT_ACTIVITY_CREATED,
    EVENT_ACTIVITY_GROUP_CREATED,
    EVENT_ACTIVITY_ORDER_STATUS_UPDATED,
)
from server.utils.analytics_utils.mixins import (
    TrackAdminCreateMixin,
    TrackAdminFieldUpdateMixin,
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
class SchoolActivityOrderAdmin(TrackAdminFieldUpdateMixin, admin.ModelAdmin):
    tracker_on_field_update_event_name = EVENT_ACTIVITY_ORDER_STATUS_UPDATED
    tracker_props_fields = ["slug", "activity__slug", "school__slug", "status"]
    tracker_fields_rename = {
        "activity__slug": "activity_slug",
        "school__slug": "school_slug",
    }
    tracker_field_to_track = "status"

    list_display = ["school", "activity", "created_at", "updated_at", "status"]
    search_fields = ["school__name", "activity__name"]
    list_filter = ["status"]
    actions = [approve_order]


@admin.register(Activity)
class ActivityAdmin(TrackAdminCreateMixin, admin.ModelAdmin):

    tracker_on_create_event_name = EVENT_ACTIVITY_CREATED
    tracker_props_fields = ["slug", "name", "domain"]

    list_display = ["slug", "name", "originization", "tags"]
    search_fields = ["name"]


@admin.register(SchoolActivityGroup)
class SchoolActivityGroupAdmin(TrackAdminCreateMixin, admin.ModelAdmin):
    tracker_on_create_event_name = EVENT_ACTIVITY_GROUP_CREATED
    tracker_props_fields = ["slug", "name", "group_type", "activity_order__slug"]
    tracker_fields_rename = {"activity_order__slug": "activity_order_slug"}

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


admin.site.register(Organization)
admin.site.register(ActivityMedia)
admin.site.register(OrganizationMember)
admin.site.register(ImportedOrganization)
admin.site.register(ImportedActivity)
