from django.contrib import admin

from .models import (
    Activity,
    ActivityMedia,
    Organization,
    OrganizationMember,
    SchoolActivityOrder,
)

admin.site.register(Organization)
admin.site.register(Activity)
admin.site.register(ActivityMedia)
admin.site.register(OrganizationMember)
admin.site.register(SchoolActivityOrder)
