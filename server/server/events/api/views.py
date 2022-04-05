import logging
from typing import Dict

from django.contrib.auth import get_user_model
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets

from server.events.api.renderers import EventCSVRenderer
from server.events.models import ConsumerEventFeedback, Event, EventOrder
from server.schools.models import School
from server.users.api_helpers import (
    PrivilegeAccessMixin,
    get_privilege_permission_classes,
    has_privilege,
)
from server.users.models import RoleScope
from server.utils.db_utils import (
    get_additional_permissions_readonly,
    get_additional_permissions_write,
)
from server.utils.permission_classes import (
    AllowConsumer,
    AllowConsumerReadOnly,
    AllowInstructor,
)
from server.utils.privileges import (
    PRIV_EVENT_EDIT,
    PRIV_EVENT_ORDER_APPROVE,
    PRIV_EVENT_ORDER_CREATE,
    PRIV_EVENT_ORDER_EDIT,
    PRIV_EVENT_ORDER_VIEW,
    PRIV_EVENT_VIEW,
)

from .serializers import (
    ConsumerEventFeedbackSerializer,
    ConsumerEventSerializer,
    EventOrderSerializer,
    EventSerializer,
)

logger = logging.getLogger(__name__)


class EventOrderViewSet(viewsets.ModelViewSet, PrivilegeAccessMixin):
    privileges_read = [PRIV_EVENT_ORDER_VIEW]
    privileges_write = [PRIV_EVENT_ORDER_EDIT]

    permission_classes = [
        get_additional_permissions_write()
        | get_privilege_permission_classes(privileges_read, privileges_write)
    ]
    serializer_class = EventOrderSerializer
    lookup_field = "slug"
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
        DjangoFilterBackend,
    ]
    search_fields = [
        "status",
        "status_reason",
        "school_group__name",
        "school_group__activity_order__school__name",
        "school_group__activity_order__activity__name",
    ]

    def get_queryset(self):
        result = EventOrder.objects.filter(school_group__isnull=False).order_by(
            "-start_time"
        )
        if self.is_admin_scope(self.request):
            return result
        organizations = self.get_allowed_organizations(self.request)
        schools = self.get_allowed_schools(self.request)
        return result.filter(
            Q(school_group__activity_order__activity__originization__in=organizations)
            | Q(school_group__activity_order__school__in=schools)
            | Q(school__in=schools)
        )

    def perform_create(self, serializer):
        # create new event order. If the user has permission to approve orders for this organization,
        # or this is no-organization order, then set status to APPROVED.
        # Otherwise, set status to PENDING_APPROVAL.

        # verify the user has permissions to create event orders:
        if not has_privilege(PRIV_EVENT_ORDER_CREATE):
            raise PermissionError(
                "User does not have privilege to create event orders."
            )
        status: EventOrder.Status = EventOrder.Status.PENDING_APPROVAL
        school: School = None
        user = self.request.user
        if "school_group" not in serializer.validated_data:
            # no school group specified, so this is a no-organization order ==> set status to APPROVED
            logger.info("no school group specified, set status to APPROVED")
            status = EventOrder.Status.APPROVED
            school = user.school_member.school
        else:
            school = serializer.validated_data["school_group"].activity_order.school
            organization = serializer.validated_data[
                "school_group"
            ].activity_order.activity.originization
            user_scopes: Dict[str, RoleScope] = user.get_privilege_scopes()
            if PRIV_EVENT_ORDER_APPROVE in user_scopes and (
                user_scopes[PRIV_EVENT_ORDER_APPROVE].is_admin_scope()
                or organization
                in user_scopes[PRIV_EVENT_ORDER_APPROVE].get_organizations()
            ):
                logger.info(
                    "user has permissions to approve orders in this organization, set status to APPROVED"
                )
                status = EventOrder.Status.APPROVED
        logger.info(f"Saving new order with status={status}")
        serializer.save(status=status, school=school)


class EventViewSet(viewsets.ModelViewSet, PrivilegeAccessMixin):
    privileges_read = [PRIV_EVENT_VIEW]
    privileges_write = [PRIV_EVENT_EDIT]

    permission_classes = [
        AllowInstructor
        | get_additional_permissions_write()
        | get_privilege_permission_classes(privileges_read, privileges_write)
    ]

    serializer_class = EventSerializer
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
        DjangoFilterBackend,
    ]
    lookup_field = "slug"
    filterset_fields = {
        "start_time": ["gte", "lte"],
        "has_summary": ["exact"],
        "is_canceled": ["exact"],
    }

    def get_queryset(self):
        user = self.request.user
        base_queryset = (
            Event.objects.select_related("event_order")
            .select_related("event_order__school_group")
            .select_related("school_group")
            .select_related("school_group__instructor")
            .select_related("school_group__activity_order")
            .select_related("school_group__activity_order__activity")
            .prefetch_related("consumers")
            .all()
            .order_by("-start_time")
        )
        my_school_only: bool = self.request.query_params.get("my_school_only", False)
        if my_school_only:
            my_school: School = self.request.user.school_member.school
            return base_queryset.filter(event_order__school__in=my_school)
        # TODO - move instructor API to a separate endpoint
        if user.user_type == get_user_model().Types.INSTRUCTOR:
            return base_queryset.filter(instructor=user)
        if self.is_admin_scope(self.request):
            return base_queryset

        organizations = self.get_allowed_organizations(self.request)
        schools = self.get_allowed_schools(self.request)

        return base_queryset.filter(
            Q(school_group__activity_order__activity__originization__in=organizations)
            | Q(event_order__school__in=schools)
        )


class ExportEventViewSet(EventViewSet):
    renderer_classes = (EventCSVRenderer,)


class ConsumerEventViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowConsumerReadOnly | get_additional_permissions_readonly()]
    serializer_class = ConsumerEventSerializer
    lookup_field = "slug"
    filterset_fields = {
        "start_time": ["gte", "lte"],
    }

    def get_queryset(self):
        return Event.objects.filter(school_group__consumers=self.request.user)


class ConsumerEventFeedbackViewset(viewsets.ModelViewSet):
    permission_classes = [AllowConsumer | get_additional_permissions_write()]
    serializer_class = ConsumerEventFeedbackSerializer
    lookup_field = "slug"

    def get_queryset(self):
        return ConsumerEventFeedback.objects.filter(consumer=self.request.user)

    def perform_create(self, serializer):
        serializer.save(consumer=self.request.user)

    def perform_update(self, serializer):
        serializer.save(consumer=self.request.user)
