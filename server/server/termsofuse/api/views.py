from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet

from ..models import TermsOfUseDocument
from .serializers import TermsOfUseDocumentSerializer


class TermsOfUseDocumentViewSet(ListModelMixin, GenericViewSet):
    permission_classes = [AllowAny]
    serializer_class = TermsOfUseDocumentSerializer
    queryset = TermsOfUseDocument.objects.filter(is_active=True)
