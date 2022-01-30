import csv
import io
from typing import List

from django import forms
from django.contrib import admin, messages
from django.shortcuts import render
from django.urls import path

from .models import ConnectiveTag, ConnectiveTaggedItem

admin.site.register(ConnectiveTaggedItem)


class TagsFileUploadForm(forms.Form):

    file = forms.FileField()


class TagFileLoader:
    def __init__(self, csv_file):
        self.csv_file = csv_file
        self.reader = csv.DictReader(
            io.StringIO(self.csv_file.read().decode(encoding="utf-8-sig"), newline=None)
        )
        self.added: List = []
        self.already_exists: List = []
        self.errors: List = []

    def get_cell_value(self, row: dict, column: str, mandatory: bool) -> str:
        result = row.get(column).strip() if row.get(column) else ""
        if not result and mandatory:
            raise Exception(f"No value for mandatory column: {column}. Row: {row}")
        return result

    def create_new_tags(self):
        row_index = 0
        for row in self.reader:
            row_index += 1
            category: str = self.get_cell_value(row, "category", True)
            name: str = self.get_cell_value(row, "name", True)
            try:
                if ConnectiveTag.objects.filter(slug=name).exists():
                    self.already_exists.append(name)
                else:
                    ConnectiveTag.objects.create(
                        category=category, name=name, slug=name
                    )
                    self.added.append(name)
            except Exception:
                self.errors.append(name)
            print(f"created: {category}:{name}")


@admin.register(ConnectiveTag)
class ConnectiveTagAdmin(admin.ModelAdmin):
    list_display = ["slug", "name", "category"]
    search_fields = ["slug", "name", "category"]

    def import_tags_from_csv(self, request):
        if request.method == "POST":  # file uploaded
            form: TagsFileUploadForm = TagsFileUploadForm(request.POST)
            form.is_valid()  # run validation without check results
            file = request.FILES["file"]
            try:
                loader: TagFileLoader = TagFileLoader(file)
                loader.create_new_tags()
                self.message_user(
                    request, f"Tags loaded: {len(loader.added)}", level=messages.INFO
                )
                if loader.already_exists:
                    self.message_user(
                        request,
                        f"Tags already exists: {len(loader.already_exists)}",
                        level=messages.WARNING,
                    )
                if loader.errors:
                    self.message_user(
                        request,
                        f"Tags failed to load: {len(loader.errors)}",
                        level=messages.ERROR,
                    )
            except Exception as e:
                self.message_user(
                    request,
                    f"File load error. Make sure you upload CSV file include 2 columns: category, name. Error: {e}",
                    level=messages.ERROR,
                )
        form = TagsFileUploadForm()
        payload = {"form": form}
        return render(request, "admin/file_upload_form.html", payload)

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path("import-from-csv/", self.import_tags_from_csv),
        ]
        return my_urls + urls
