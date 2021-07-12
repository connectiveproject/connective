from django.contrib import admin

from .models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ["school_group", "start_time", "end_time", "school", "activity"]

    def school(self, obj):
        return obj.school_group.activity_order.school

    def activity(self, obj):
        return obj.school_group.activity_order.activity
