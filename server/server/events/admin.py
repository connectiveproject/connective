import logging

from django.contrib import admin

from .models import ConsumerEventFeedback, Event

logger = logging.getLogger(__name__)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ["school_group", "start_time", "end_time", "school", "activity"]

    def school(self, obj):
        try:
            return obj.school_group.activity_order.school
        except AttributeError as err:
            logger.warn(err)

    def activity(self, obj):
        try:
            return obj.school_group.activity_order.activity
        except AttributeError as err:
            logger.warn(err)


admin.site.register(ConsumerEventFeedback)
