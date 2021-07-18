import logging

from django.contrib import admin

from .models import ConsumerEventFeedback, Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ["school_group", "start_time", "end_time", "school", "activity"]
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
            logging.getLogger("root").warning(
                f"event {obj.slug} has no school_group attribute"
            )

    def activity(self, obj):
        try:
            return obj.school_group.activity_order.activity

        except AttributeError:
            logging.getLogger("root").warning(
                f"event {obj.slug} has no school_group attribute"
            )


admin.site.register(ConsumerEventFeedback)
