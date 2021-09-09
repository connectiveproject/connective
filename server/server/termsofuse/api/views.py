from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet

from ..models import TermsOfUseDocument
from .serializers import TermsOfUseDocumentSerializer


class TermsOfUseDocumentViewSet(ListModelMixin, GenericViewSet):
    permission_classes = [AllowAny]
    serializer_class = TermsOfUseDocumentSerializer

    def get_queryset(self):
        if TermsOfUseDocument.objects.count():
            return TermsOfUseDocument.objects.filter(
                slug=TermsOfUseDocument.objects.last().slug
            )
        return TermsOfUseDocument.objects.none()
