from django import forms
from django.contrib import admin
from django.core.exceptions import ValidationError

from .models import TermsOfUseDocument, TermsOfUsePeriod


class TermsOfUseDocumentAdminForm(forms.ModelForm):
    class Meta:
        model = TermsOfUseDocument
        fields = "__all__"

    def clean(self):
        if (
            not self.cleaned_data["is_active"]
            and not TermsOfUseDocument.objects.filter(is_active=True)
            .exclude(slug=self.cleaned_data["slug"])
            .exists()
        ):
            raise ValidationError("model must contain at least one active document")
        return self.cleaned_data


@admin.register(TermsOfUseDocument)
class TermsOfUseDocumentAdmin(admin.ModelAdmin):
    form = TermsOfUseDocumentAdminForm
    list_display = [
        "document_name",
        "document_text_trimmed",
        "is_active",
        "created",
        "updated",
    ]

    def document_text_trimmed(self, obj):
        return obj.document_text[:150]


@admin.register(TermsOfUsePeriod)
class TermsOfUsePeriod(admin.ModelAdmin):
    list_display = ["document", "document_name", "start_date", "end_date"]

    def document_name(self, obj):
        if obj.document:
            return obj.document.document_name
        return "<deleted>"
