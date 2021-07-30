import logging

from django.contrib import admin

from .models import ConsumerEventFeedback, Event, EventOrder

logger = logging.getLogger(__name__)


def approve_order(self, request, queryset):
    for order in queryset:
        order.status = EventOrder.Status.APPROVED
        order.save()


approve_order.short_description = "Approve Selected Orders"


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = [
        "school_group",
        "start_time",
        "end_time",
        "school",
        "activity",
        "has_summary",
    ]
    search_fields = [
        "school_group__activity_order__school__name",
        "school_group__activity_order__activity__name",
        "school_group__name",
    ]
    list_filter = ["school_group__name"]

    def school(self, obj):
        try:
            return obj.school_group.activity_order.school
        except AttributeError:
            logger.error(f"event {obj.slug} has no school_group attribute")

    def activity(self, obj):
        try:
            return obj.school_group.activity_order.activity
        except AttributeError:
            logger.error(f"event {obj.slug} has no school_group attribute")


@admin.register(EventOrder)
class EventOrderAdmin(admin.ModelAdmin):
    list_display = [
        "slug",
        "school_group",
        "start_time",
        "end_time",
        "school",
        "activity",
        "recurrence",
        "status",
        "created",
        "updated",
        "locations_name",
    ]
    list_filter = ["status", "school_group__name"]
    actions = [approve_order]

    def school(self, obj):
        try:
            return obj.school_group.activity_order.school
        except AttributeError:
            logger.error(f"event {obj.slug} has no school_group attribute")

    def activity(self, obj):
        try:
            return obj.school_group.activity_order.activity
        except AttributeError:
            logger.error(f"event {obj.slug} has no school_group attribute")


admin.site.register(ConsumerEventFeedback)
