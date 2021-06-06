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
    ConsumerActivitySerializer,
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
    permission_classes = [AllowAllDebug]
    serializer_class = ActivitySerializer
    lookup_field = "slug"

    queryset = Activity.objects.all()


class ConsumerActivityViewSet(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    permission_classes = [AllowAllDebug]
    serializer_class = ConsumerActivitySerializer
    lookup_field = "slug"

    def get_queryset(self):
        user = self.request.user
        if not user.user_type == user.Types.CONSUMER:
            return Activity.objects.none()

        approved_orders = SchoolActivityOrder.objects.filter(
            school=user.school_member.school,
            status=SchoolActivityOrder.Status.APPROVED,
        ).values("activity")
        return Activity.objects.filter(id__in=approved_orders)


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
