from django.contrib import admin

from .models import School, SchoolMember


class SchoolMemberTabularInline(admin.TabularInline):
    model = SchoolMember
    min_num = 1


admin.site.register(School)
admin.site.register(SchoolMember)
