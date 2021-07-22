from contextlib import suppress

from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from server.organizations.models import (
    Activity,
    ActivityMedia,
    Organization,
    SchoolActivityGroup,
    SchoolActivityOrder,
)
from server.users.api.serializers import UserSerializer
from server.utils.permission_classes import (
    AllowConsumer,
    AllowConsumerReadOnly,
    AllowCoordinator,
    AllowCoordinatorReadOnly,
    AllowInstructorReadOnly,
    AllowVendor,
)

from .filters import ActivityFilter
from .serializers import (
    ActivityMediaSerializer,
    ActivitySerializer,
    ConsumerActivitySerializer,
    ConsumerRequestDataSerializer,
    ManageSchoolActivitySerializer,
    OrganizationSerializer,
    SchoolActivityGroupSerializer,
    VendorActivitySerializer,
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


class ActivityViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowCoordinatorReadOnly]
    serializer_class = ActivitySerializer
    lookup_field = "slug"
    filterset_class = ActivityFilter
    search_fields = ["name", "description"]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]

    queryset = Activity.objects.all()


class VendorActivityViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowVendor]
    serializer_class = VendorActivitySerializer
    lookup_field = "slug"

    def get_queryset(self):
        user = self.request.user
        return Activity.objects.filter(
            originization=user.organization_member.organization,
        )

    def perform_create(self, serializer):
        serializer.save(
            originization=self.request.user.organization_member.organization
        )

    def perform_update(self, serializer):
        serializer.save(
            originization=self.request.user.organization_member.organization
        )


class ConsumerActivityViewSet(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    permission_classes = [AllowConsumer]
    serializer_class = ConsumerActivitySerializer
    lookup_field = "slug"
    filterset_class = ActivityFilter
    search_fields = ["name", "description", "tags__name"]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_fields = ["tags"]

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
    permission_classes = [
        AllowVendor
        | AllowCoordinatorReadOnly
        | AllowInstructorReadOnly
        | AllowConsumerReadOnly
    ]
    serializer_class = ActivityMediaSerializer
    lookup_field = "slug"
    queryset = ActivityMedia.objects.all()
    filterset_fields = ("activity__slug",)


class ManageSchoolActivityViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowCoordinator]
    serializer_class = ManageSchoolActivitySerializer
    lookup_field = "activity__slug"
    filterset_fields = ("status",)

    def get_queryset(self):
        coord_school = self.request.user.school_member.school
        return SchoolActivityOrder.objects.filter(school=coord_school)

    def perform_create(self, serializer):
        serializer.save(
            requested_by=self.request.user, last_updated_by=self.request.user
        )

    def perform_update(self, serializer):
        serializer.save(last_updated_by=self.request.user)


class SchoolActivityGroupViewSet(viewsets.ModelViewSet):
    permission_classes = [
        AllowCoordinator | AllowConsumerReadOnly | AllowInstructorReadOnly
    ]
    serializer_class = SchoolActivityGroupSerializer
    queryset = SchoolActivityOrder.objects.all()
    filterset_fields = ["group_type", "activity_order__slug"]
    lookup_field = "slug"

    def get_queryset(self):
        user = self.request.user
        if user.user_type == get_user_model().Types.CONSUMER:
            return SchoolActivityGroup.objects.filter(consumers=user)

        if user.user_type == get_user_model().Types.INSTRUCTOR:
            return SchoolActivityGroup.objects.filter(instructor=user)

        return SchoolActivityGroup.objects.filter(
            activity_order__in=user.school_member.school.school_activity_orders.all(),
        )

    @action(detail=True, methods=["GET"])
    def group_consumers(self, request, slug=None):
        serializer = UserSerializer(
            self.get_object().consumers,
            context={"request": request},
            many=True,
        )
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    @action(detail=True, methods=["PATCH"])
    def update_group_consumers(self, request, slug=None):
        # receive consumer slugs list, override existing consumers & move the removed to container-only group
        current_group = self.get_object()
        container_only_group = (
            SchoolActivityGroup.objects.get_activity_container_only_group(current_group)
        )
        if not container_only_group:
            return Response(
                {"non_field_errors": ["container group could not be found"]},
                status=status.HTTP_400_BAD_REQUEST,
            )

        to_remove = current_group.consumers.all().exclude(slug__in=request.data)
        to_add = container_only_group.consumers.all().filter(slug__in=request.data)

        current_group.consumers.remove(*to_remove)
        current_group.consumers.add(*to_add)

        container_only_group.consumers.remove(*to_add)
        container_only_group.consumers.add(*to_remove)

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=["GET"])
    def consumer_requests_data(self, request):
        """
        requests to each activity, based on container_only consumers
        """
        qs = (
            self.get_queryset()
            .filter(group_type=SchoolActivityGroup.GroupTypes.CONTAINER_ONLY)
            .annotate(consumer_requests=Count("consumers"))
            .order_by("-consumer_requests")[:10]
        )
        return Response(ConsumerRequestDataSerializer(qs, many=True).data)
