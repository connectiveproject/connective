from django.core.exceptions import ObjectDoesNotExist
from rest_framework import mixins, viewsets

from server.organizations.models import (
    Activity,
    ActivityMedia,
    Organization,
    SchoolActivityOrder,
)
from server.utils.permission_classes import AllowAllDebug

from .serializers import (
    ActivityMediaSerializer,
    ActivitySerializer,
    ManageSchoolActivitySerializer,
    OrganizationSerializer,
)


class OrganizationViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = OrganizationSerializer
    lookup_field = "slug"

    def get_queryset(self):
        try:
            Organization.objects.filter(
                organization_member__in=[self.request.user.organization_member]
            )

        except ObjectDoesNotExist:
            return Organization.objects.none()


class ActivityViewSet(viewsets.ModelViewSet):
    serializer_class = ActivitySerializer
    lookup_field = "slug"

    queryset = Activity.objects.all()


class ActivityMediaViewSet(viewsets.ModelViewSet):
    serializer_class = ActivityMediaSerializer
    lookup_field = "slug"
    queryset = ActivityMedia.objects.all()
    filterset_fields = ("activity__slug",)


class ManageSchoolActivityViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAllDebug]
    serializer_class = ManageSchoolActivitySerializer
    lookup_field = "activity__slug"

    queryset = SchoolActivityOrder.objects.all()

    def perform_create(self, serializer):
        serializer.save(
            requested_by=self.request.user, last_updated_by=self.request.user
        )

    def perform_update(self, serializer):
        serializer.save(last_updated_by=self.request.user)
