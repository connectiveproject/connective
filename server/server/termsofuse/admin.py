from django.contrib import admin

from .models import TermsOfUseDocument, TermsOfUseSignature


@admin.register(TermsOfUseDocument)
class TermsOfUseDocumentAdmin(admin.ModelAdmin):
    list_display = [
        "document_name",
        "document_text_trimmed",
        "created",
    ]

    def document_text_trimmed(self, obj):
        return obj.document_text[:150]


@admin.register(TermsOfUseSignature)
class TermsOfUseSignature(admin.ModelAdmin):
    list_display = ["document", "document_name", "user", "created"]

    def document_name(self, obj):
        if obj.document:
            return obj.document.document_name
        return "<deleted>"
