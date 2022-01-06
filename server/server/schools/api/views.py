from django.core.exceptions import ObjectDoesNotExist
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from server.utils.db_utils import get_additional_permissions_write
from server.utils.permission_classes import AllowConsumerReadOnly, AllowCoordinator

from ..models import School
from .serializers import SchoolSerializer


class SchoolViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    permission_classes = [
        AllowCoordinator | AllowConsumerReadOnly | get_additional_permissions_write()
    ]
    serializer_class = SchoolSerializer
    lookup_field = "slug"

    def get_queryset(self):
        try:
            return School.objects.filter(
                school_member__in=[self.request.user.school_member]
            )
        except ObjectDoesNotExist:
            return School.objects.none()

    def perform_create(self, serializer):
        serializer.save(last_updated_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(last_updated_by=self.request.user)

    @action(detail=False, methods=["GET"])
    def me(self, request):
        serializer = SchoolSerializer(
            request.user.school_member.school, context={"request": request}
        )
        return Response(status=status.HTTP_200_OK, data=serializer.data)
