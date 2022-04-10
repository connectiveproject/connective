from contextlib import suppress

import analytics
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count, Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from server.connective_tags.views import TagsAllFilter
from server.organizations.models import (
    Activity,
    ActivityMedia,
    Organization,
    SchoolActivityGroup,
    SchoolActivityOrder,
)
from server.organizations.signals import activity_order_created_signal
from server.users.api.serializers import UserSerializer
from server.users.api_helpers import (
    PrivilegeAccessMixin,
    get_privilege_permission_classes,
    has_any_privilege,
)
from server.users.models import Consumer
from server.utils.analytics_utils import event
from server.utils.db_utils import get_additional_permissions_write
from server.utils.permission_classes import (
    AllowConsumer,
    AllowConsumerReadOnly,
    AllowCoordinator,
    AllowCoordinatorReadOnly,
    AllowInstructorReadOnly,
    AllowVendor,
)
from server.utils.privileges import (
    PRIV_ACTIVITY_EDIT,
    PRIV_ACTIVITY_VIEW,
    PRIV_ACTIVITY_VIEW_ALL,
    PRIV_GROUP_MANAGE_ORGANIZATION_EDIT,
    PRIV_GROUP_MANAGE_ORGANIZATION_VIEW,
    PRIV_GROUP_MANAGE_SCHOOL_EDIT,
    PRIV_GROUP_MANAGE_SCHOOL_VIEW,
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
    permission_classes = [
        AllowCoordinatorReadOnly | AllowVendor | get_additional_permissions_write()
    ]
    serializer_class = OrganizationSerializer
    lookup_field = "slug"

    def get_queryset(self):
        try:
            return Organization.objects.filter(
                organization_member__in=[self.request.user.organization_member]
            )

        except ObjectDoesNotExist:
            return Organization.objects.none()


class ActivityViewSet(viewsets.ReadOnlyModelViewSet, PrivilegeAccessMixin):

    privileges_read = [PRIV_ACTIVITY_VIEW, PRIV_ACTIVITY_VIEW_ALL]
    privileges_write = [PRIV_ACTIVITY_EDIT]

    permission_classes = [
        get_privilege_permission_classes(privileges_read, privileges_write)
    ]
    serializer_class = ActivitySerializer
    lookup_field = "slug"
    filterset_class = ActivityFilter
    search_fields = ["name", "description"]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, TagsAllFilter]

    def get_queryset(self):
        queryset = Activity.objects.prefetch_related("tags").all()
        if self.is_admin_scope(self.request) or has_any_privilege(
            [PRIV_ACTIVITY_VIEW_ALL], self.request.user
        ):
            return queryset
        organizations = self.get_allowed_organizations(self.request)
        return queryset.filter(originization__in=organizations)


class VendorActivityViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowVendor | get_additional_permissions_write()]
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
    permission_classes = [AllowConsumer | get_additional_permissions_write()]
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
        return Activity.objects.filter(id__in=approved_orders).order_by("-id")

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
        | get_additional_permissions_write()
    ]
    serializer_class = ActivityMediaSerializer
    lookup_field = "slug"
    queryset = ActivityMedia.objects.all()
    filterset_fields = ("activity__slug",)


class ManageSchoolActivityViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowCoordinator | get_additional_permissions_write()]
    serializer_class = ManageSchoolActivitySerializer
    lookup_field = "activity__slug"
    filterset_fields = ("status",)

    def get_queryset(self):
        coord_school = self.request.user.school_member.school
        return SchoolActivityOrder.objects.filter(school=coord_school).order_by("-id")

    def perform_create(self, serializer):
        newOrder: SchoolActivityOrder = serializer.save(
            requested_by=self.request.user, last_updated_by=self.request.user
        )
        activity_order_created_signal.send(
            sender=self.__class__, activity_order=newOrder
        )

    def perform_update(self, serializer):
        serializer.save(last_updated_by=self.request.user)


class SchoolActivityGroupViewSet(viewsets.ModelViewSet, PrivilegeAccessMixin):
    privileges_read_school = [PRIV_GROUP_MANAGE_SCHOOL_VIEW]
    privileges_write_school = [PRIV_GROUP_MANAGE_SCHOOL_EDIT]
    privileges_read_organization = [PRIV_GROUP_MANAGE_ORGANIZATION_VIEW]
    privileges_write_organization = [PRIV_GROUP_MANAGE_ORGANIZATION_EDIT]

    permission_classes = [
        get_privilege_permission_classes(
            privileges_read_school, privileges_write_school
        )
        | get_privilege_permission_classes(
            privileges_read_organization, privileges_write_organization
        )
    ]

    serializer_class = SchoolActivityGroupSerializer
    filterset_fields = ["group_type", "activity_order__slug"]
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
        DjangoFilterBackend,
    ]
    search_fields = [
        "name",
        "description",
        "instructor__name",
        "activity_order__school__name",
        "activity_order__activity__name",
    ]
    filterset_fields = [
        "activity_order__school__slug",
    ]
    lookup_field = "slug"

    def get_queryset(self):
        user = self.request.user
        queryset = SchoolActivityGroup.objects.all()
        if self.is_admin_scope(self.request):
            return queryset
        organizations = self.get_allowed_organizations(self.request)
        schools = self.get_allowed_schools(self.request)
        filter = Q(activity_order__activity__originization__in=organizations) | Q(
            activity_order__school__in=schools
        )
        if user.user_type == get_user_model().Types.CONSUMER:
            filter = filter | Q(consumers=user)
        return queryset.filter(filter)

    @action(detail=False, methods=["GET"])
    def group_consumers(self, request):
        slugs = request.query_params.get("slugs")
        if not slugs:
            return Response(
                "group slugs must be specified", status=status.HTTP_400_BAD_REQUEST
            )

        queryset = Consumer.objects.filter(activity_groups__slug__in=slugs.split(","))
        page = self.paginate_queryset(queryset)
        if page is not None:
            # if pagination is allowed in the project
            serializer = UserSerializer(
                page,
                context={"request": request},
                many=True,
            )
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    @action(detail=True, methods=["PATCH"])
    def update_group_consumers(self, request, slug=None):
        """
        receive consumer slugs list, override existing consumers & move the removed to container-only group
        """
        current_group = self.get_object()
        container_only_group = (
            SchoolActivityGroup.objects.get_activity_container_only_group(current_group)
        )

        to_remove = current_group.consumers.all().exclude(slug__in=request.data)
        to_add = Consumer.objects.filter(slug__in=request.data)

        current_group.consumers.remove(*to_remove)
        current_group.consumers.add(*to_add)

        if container_only_group:
            container_only_group.consumers.remove(*to_add)
            container_only_group.consumers.add(*to_remove)

        analytics.track(
            request.user.slug,
            event.ACTIVITY_GROUP_CONSUMER_LIST_CHANGED,
            {
                "slug": slug,
                "name": current_group.name,
                "group_type": current_group.group_type,
                "activity_order_slug": current_group.activity_order.slug,
                "consumers_count": current_group.consumers.count(),
            },
        )
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=["GET"])
    def consumer_requests_data(self, request):
        """
        requests to each activity, based on container_only consumers
        """
        top = request.query_params.get("top")
        if top and top.isdigit():
            top = int(top)
        else:
            top = 10

        qs = (
            self.get_queryset()
            .filter(group_type=SchoolActivityGroup.GroupTypes.CONTAINER_ONLY)
            .annotate(consumer_requests=Count("consumers"))
            .order_by("-consumer_requests")[:top]
        )
        return Response(ConsumerRequestDataSerializer(qs, many=True).data)
