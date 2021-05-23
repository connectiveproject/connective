from django.contrib import admin

from .models import Activity, ActivityMedia, Organization, OrganizationMember

admin.site.register(Organization)
admin.site.register(Activity)
admin.site.register(ActivityMedia)
admin.site.register(OrganizationMember)
