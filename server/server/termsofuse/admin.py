from django.contrib import admin

from .models import TermsOfUseDocument, TermsOfUsePeriod


@admin.register(TermsOfUseDocument)
class TermsOfUseDocumentAdmin(admin.ModelAdmin):
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
