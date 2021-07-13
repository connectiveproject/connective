from django.contrib import admin

from .models import (
    Activity,
    ActivityMedia,
    Organization,
    OrganizationMember,
    SchoolActivityGroup,
    SchoolActivityOrder,
)


def approve_order(self, request, queryset):
    for order in queryset:
        order.status = SchoolActivityOrder.Status.APPROVED
        order.save()


approve_order.short_description = "Approve Selected Orders"


class OrganizationMemberTabularInline(admin.TabularInline):
    model = OrganizationMember
    min_num = 1


@admin.register(SchoolActivityOrder)
class SchoolActivityOrderAdmin(admin.ModelAdmin):
    list_display = ["school", "activity", "created_at", "updated_at", "status"]
    search_fields = ["school__name", "activity__name"]
    actions = [approve_order]


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ["slug", "name", "originization", "tags"]
    search_fields = ["name"]


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

    def school(self, obj):
        return obj.activity_order.school

    def activity(self, obj):
        return obj.activity_order.activity


admin.site.register(Organization)
admin.site.register(ActivityMedia)
admin.site.register(OrganizationMember)
