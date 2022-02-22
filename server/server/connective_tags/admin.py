from django import forms
from django.contrib import admin
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import path

from server.utils.admin_utils import (
    AdminCSVFileLoader,
    AdminFileUploadForm,
    import_entities_from_csv,
)

from .models import ConnectiveTag, ConnectiveTaggedItem

admin.site.register(ConnectiveTaggedItem)


class TagsFileUploadForm(forms.Form):

    file = forms.FileField()


class TagFileLoader(AdminCSVFileLoader):
    def get_tag_name(self, row) -> str:
        return self.get_cell_value(row, "name", True)

    def get_tag_category(self, row) -> str:
        return self.get_cell_value(row, "category", True)

    def check_if_exists(self, row):
        name: str = self.get_tag_name(row)
        return ConnectiveTag.objects.filter(slug=name).exists()

    def create_new(self, row):
        name: str = self.get_tag_name(row)
        category: str = self.get_tag_category(row)
        ConnectiveTag.objects.create(category=category, name=name, slug=name)

    def row_to_str(self, row):
        return self.get_tag_name(row)

    def file_error_message(self) -> str:
        return "Make sure you upload CSV file include 2 columns: category, name."

    def entities_name(self) -> str:
        return "Tags"


@admin.register(ConnectiveTag)
class ConnectiveTagAdmin(admin.ModelAdmin):
    list_display = ["slug", "name", "category"]
    search_fields = ["slug", "name", "category"]

    def export_tags_to_csv(self, request) -> HttpResponse:
        csv_text: str = "category,name\r\n"
        for tag in ConnectiveTag.objects.all():
            csv_text += f"{tag.category},{tag.name}\r\n"
        response = HttpResponse(
            csv_text, content_type="content_type='application/octet-stream'"
        )
        response["Content-Disposition"] = 'attachment; filename="tags.csv"'
        return response

    def import_tags_from_csv(self, request) -> HttpResponse:
        if request.method == "POST":  # file uploaded
            form: AdminFileUploadForm = AdminFileUploadForm(request.POST)
            form.is_valid()  # run validation without check results
            file = request.FILES["file"]
            import_entities_from_csv(self, request, TagFileLoader(), file)
        form = AdminFileUploadForm()
        payload = {"form": form}
        return render(request, "admin/file_upload_form.html", payload)

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path("import-from-csv/", self.import_tags_from_csv),
            path("export-to-csv/", self.export_tags_to_csv),
        ]
        return my_urls + urls
