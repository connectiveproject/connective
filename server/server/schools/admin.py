from django.contrib import admin
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import path

from server.utils.admin_utils import (
    AdminCSVFileLoader,
    AdminFileUploadForm,
    import_entities_from_csv,
)

from .models import ImportedSchool, School, SchoolMember


class SchoolCSVFileLoader(AdminCSVFileLoader):
    def parse_school_code(self, row) -> str:
        return self.get_cell_value(row, "school_code", True)

    def parse_school_name(self, row) -> str:
        return self.get_cell_value(row, "name", True)

    def check_if_exists(self, row):
        name: str = self.parse_school_name(row)
        code: str = self.parse_school_code(row)
        return School.objects.filter(Q(name=name) | Q(school_code=code)).exists()

    def create_new(self, row):
        name: str = self.parse_school_name(row)
        school_code: str = self.parse_school_code(row)
        address: str = self.get_cell_value(row, "address", True)
        address_city: str = self.get_cell_value(row, "address_city", True)
        contact_phone: str = self.get_cell_value(row, "contact_phone", True)
        School.objects.create(
            name=name,
            school_code=school_code,
            address=address,
            address_city=address_city,
            contact_phone=contact_phone,
            grade_levels=[],
        )

    def row_to_str(self, row):
        return f"{self.parse_school_name(row)} ({self.parse_school_code(row)})"

    def file_error_message(self) -> str:
        return "Make sure you upload CSV file include 5 columns: name, school_code, address, \
            address_city, contact_phone."

    def entities_name(self) -> str:
        return "Schools"


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    exclude = ["last_updated_by"]

    def import_schools_from_csv(self, request) -> HttpResponse:
        if request.method == "POST":  # file uploaded
            form: AdminFileUploadForm = AdminFileUploadForm(request.POST)
            form.is_valid()  # run validation without check results
            file = request.FILES["file"]
            import_entities_from_csv(self, request, SchoolCSVFileLoader(), file)
        form = AdminFileUploadForm()
        payload = {"form": form}
        return render(request, "admin/file_upload_form.html", payload)

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path("import-from-csv/", self.import_schools_from_csv),
        ]
        return my_urls + urls


class SchoolMemberTabularInline(admin.TabularInline):
    model = SchoolMember
    min_num = 1


admin.site.register(SchoolMember)
admin.site.register(ImportedSchool)
