from django.core.exceptions import ObjectDoesNotExist

from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from ..models import School
from .serializers import SchoolSerializer


class SchoolViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    serializer_class = SchoolSerializer
    lookup_field = "slug"

    def get_queryset(self, *args, **kwargs):
        try:
            return School.objects.filter(
                school_member__in=[self.request.user.school_member]
            )
        except ObjectDoesNotExist:
            return School.objects.none()
