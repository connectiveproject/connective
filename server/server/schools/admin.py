from django.contrib import admin

from .models import School, SchoolMember


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    exclude = ["last_updated_by"]


class SchoolMemberTabularInline(admin.TabularInline):
    model = SchoolMember
    min_num = 1


admin.site.register(SchoolMember)
