from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from import_export.forms import ImportForm
from django import forms


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


class ActivityImportForm(ImportForm):
    organization = forms.ModelChoiceField(
        queryset=Organization.objects.all(),
        required=True)

class ActivityResource(resources.ModelResource):

    class Meta:
        model = Activity
        # import_id_fields = ('origanization__organization_number',)
        fields = [
            "id",
            "slug",
            "name",
            "target_audience",
            "domain",
            "origanization",
            "activity_website_url",
            "activity_email",
            "description",
            "contact_name",
            "logo",
            "phone_number",
        ]

@admin.register(Activity)
class ActivityAdmin(ImportExportModelAdmin):
    resource_class = ActivityResource
# @admin.register(Activity)
# class SchoolActivityOrderAdmin(admin.ModelAdmin):
#     list_display = ["school", "activity", "created_at", "updated_at", "status"]


admin.site.register(Organization)
# admin.site.register(Activity, ImportExportModelAdmin)
admin.site.register(ActivityMedia)
admin.site.register(OrganizationMember)
admin.site.register(SchoolActivityGroup)
