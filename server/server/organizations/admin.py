from django.contrib import admin

from .models import (
    Activity,
    ActivityMedia,
    Organization,
    OrganizationMember,
    SchoolActivityGroup,
    SchoolActivityOrder,
)


@admin.register(SchoolActivityOrder)
class SchoolActivityOrderAdmin(admin.ModelAdmin):
    list_display = ["school", "activity", "created_at", "updated_at", "status"]


admin.site.register(Organization)
admin.site.register(Activity)
admin.site.register(ActivityMedia)
admin.site.register(OrganizationMember)
admin.site.register(SchoolActivityGroup)
