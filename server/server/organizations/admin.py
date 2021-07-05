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


approve_order.short_description = "Approve Order"


class OrganizationMemberTabularInline(admin.TabularInline):
    model = OrganizationMember
    min_num = 1


@admin.register(SchoolActivityOrder)
class SchoolActivityOrderAdmin(admin.ModelAdmin):
    list_display = ["school", "activity", "created_at", "updated_at", "status"]
    actions = [approve_order]


admin.site.register(Organization)
admin.site.register(Activity)
admin.site.register(ActivityMedia)
admin.site.register(OrganizationMember)
admin.site.register(SchoolActivityGroup)
