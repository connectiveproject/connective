import csv
import io
import logging
from typing import List

from django import forms
from django.contrib import messages
from django.http import HttpResponse

logger = logging.getLogger(__name__)


class AdminCSVFileLoader:
    """
    Abstract class for CSV file loaders in Admin. Used to load CSV file into a model.
    """

    def load_csv_file(self, csv_file):
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

    def entities_name(self) -> str:
        # should to be overridden by sub-class
        return "Entities"

    def file_error_message(self) -> str:
        # should to be overridden by sub-class
        return ""

    def check_if_exists(self, row):
        raise NotImplementedError(
            "not implemented yet"
        )  # must be overridden by sub-class

    def create_new(self, row):
        raise NotImplementedError(
            "not implemented yet"
        )  # must be overridden by sub-class

    def row_to_str(self, row):
        raise NotImplementedError(
            "not implemented yet"
        )  # must be overridden by sub-class

    def executeImport(self):
        row_index = 0
        for row in self.reader:
            row_index += 1
            row_str = self.row_to_str(row)
            try:
                if self.check_if_exists(row):
                    self.already_exists.append(row_str)
                else:
                    self.create_new(row)
                    self.added.append(row_str)
            except Exception as err:
                self.errors.append(row_str)
                logger.error(err, f"Error while importing {row_str}")


class AdminFileUploadForm(forms.Form):

    file = forms.FileField()


def import_entities_from_csv(
    admin, request, loader: AdminCSVFileLoader, file
) -> HttpResponse:
    if request.method == "POST":  # file uploaded
        form: AdminFileUploadForm = AdminFileUploadForm(request.POST)
        form.is_valid()  # run validation without check results
        try:
            loader.load_csv_file(file)
            entities_name: str = loader.entities_name()
            loader.executeImport()
            admin.message_user(
                request,
                f"{entities_name} loaded: {len(loader.added)}",
                level=messages.INFO,
            )
            if loader.already_exists:
                admin.message_user(
                    request,
                    f"{entities_name} already exists: {len(loader.already_exists)}",
                    level=messages.WARNING,
                )
            if loader.errors:
                admin.message_user(
                    request,
                    f"{entities_name} failed to load: {len(loader.errors)}",
                    level=messages.ERROR,
                )
        except Exception as e:
            admin.message_user(
                request,
                f"File load error. {loader.file_error_message()} Error: {e}",
                level=messages.ERROR,
            )
