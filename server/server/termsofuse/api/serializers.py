from rest_framework import serializers

from ..models import TermsOfUseDocument


class TermsOfUseDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TermsOfUseDocument
        fields = ["document_text"]
        read_only_fields = ["document_text"]
