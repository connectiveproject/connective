from contextlib import suppress

from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from server.organizations.models import (
    Activity,
    ActivityMedia,
    Organization,
    SchoolActivityGroup,
    SchoolActivityOrder,
)
from server.utils.permission_classes import (
    AllowConsumer,
    AllowConsumerReadOnly,
    AllowCoordinator,
    AllowCoordinatorReadOnly,
    AllowVendor,
)

from .serializers import (
    ActivityMediaSerializer,
    ActivitySerializer,
    ConsumerActivitySerializer,
    ManageSchoolActivitySerializer,
    OrganizationSerializer,
    SchoolActivityGroupSerializer,
)


class OrganizationViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    permission_classes = [AllowCoordinatorReadOnly | AllowVendor]
    serializer_class = OrganizationSerializer
    lookup_field = "slug"

    def get_queryset(self):
        try:
            return Organization.objects.filter(
                organization_member__in=[self.request.user.organization_member]
            )

        except ObjectDoesNotExist:
            return Organization.objects.none()


class ActivityViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowCoordinator]
    serializer_class = ActivitySerializer
    lookup_field = "slug"

    queryset = Activity.objects.all()


class ConsumerActivityViewSet(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    permission_classes = [AllowConsumer]
    serializer_class = ConsumerActivitySerializer
    lookup_field = "slug"

    def get_queryset(self):
        user = self.request.user
        approved_orders = SchoolActivityOrder.objects.filter(
            school=user.school_member.school,
            status=SchoolActivityOrder.Status.APPROVED,
        ).values("activity")
        return Activity.objects.filter(id__in=approved_orders)

    @action(detail=True, methods=["POST"])
    def join_group(self, request, slug=None):
        if not hasattr(request.user, "school_member"):
            return Response(
                {"non_field_errors": ["must be a school member"]},
                status=status.HTTP_400_BAD_REQUEST,
            )
        order = SchoolActivityOrder.objects.get(
            school=request.user.school_member.school,
            activity__slug=slug,
        )

        with suppress(ObjectDoesNotExist):
            # check if user already in a group, and handle accordingly
            existing_group = SchoolActivityGroup.objects.get(
                activity_order=order,
                consumers=request.user.pk,
            )
            if (
                existing_group.group_type
                == SchoolActivityGroup.GroupTypes.DISABLED_CONSUMERS
            ):
                existing_group.consumers.remove(request.user.pk)

            else:
                return Response(
                    {"non_field_errors": ["user already in a group"]},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        group, _ = SchoolActivityGroup.objects.get_or_create(
            activity_order=order,
            group_type=SchoolActivityGroup.GroupTypes.CONTAINER_ONLY,
        )
        group.consumers.add(self.request.user.pk)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=["POST"])
    def leave_group(self, request, slug=None):
        """
        move consumer to a "disabled consumers" group
        """
        if not hasattr(request.user, "school_member"):
            return Response(
                {"non_field_errors": ["must be a school member"]},
                status=status.HTTP_400_BAD_REQUEST,
            )
        order = SchoolActivityOrder.objects.get(
            school=request.user.school_member.school,
            activity__slug=slug,
        )
        try:
            SchoolActivityGroup.objects.exclude(
                group_type=SchoolActivityGroup.GroupTypes.DISABLED_CONSUMERS
            ).get(activity_order=order, consumers=request.user.pk,).consumers.remove(
                request.user.pk
            )

        except ObjectDoesNotExist:
            return Response(
                {"non_field_errors": ["user is not in an active group"]},
                status=status.HTTP_400_BAD_REQUEST,
            )

        group, _created = SchoolActivityGroup.objects.get_or_create(
            activity_order=order,
            group_type=SchoolActivityGroup.GroupTypes.DISABLED_CONSUMERS,
        )
        group.consumers.add(request.user.pk)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ActivityMediaViewSet(viewsets.ModelViewSet):
    serializer_class = ActivityMediaSerializer
    lookup_field = "slug"
    queryset = ActivityMedia.objects.all()
    filterset_fields = ("activity__slug",)


class ManageSchoolActivityViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowCoordinator]
    serializer_class = ManageSchoolActivitySerializer
    lookup_field = "activity__slug"

    queryset = SchoolActivityOrder.objects.all()

    def perform_create(self, serializer):
        serializer.save(
            requested_by=self.request.user, last_updated_by=self.request.user
        )

    def perform_update(self, serializer):
        serializer.save(last_updated_by=self.request.user)


class SchoolActivityGroupViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowCoordinator | AllowConsumerReadOnly]
    serializer_class = SchoolActivityGroupSerializer
    queryset = SchoolActivityOrder.objects.all()
    filterset_fields = ["group_type"]

    def get_queryset(self):
        user = self.request.user
        if user.user_type == get_user_model().Types.CONSUMER:
            return SchoolActivityGroup.objects.filter(consumers=user)

        return SchoolActivityGroup.objects.filter(
            activity_order__in=user.school_member.school.school_activity_orders.all(),
        )
