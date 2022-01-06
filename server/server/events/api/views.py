from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets

from server.events.models import ConsumerEventFeedback, Event, EventOrder
from server.utils.db_utils import (
    get_additional_permissions_readonly,
    get_additional_permissions_write,
)
from server.utils.permission_classes import (
    AllowConsumer,
    AllowConsumerReadOnly,
    AllowCoordinator,
    AllowInstructor,
    AllowVendor,
)

from .serializers import (
    ConsumerEventFeedbackSerializer,
    ConsumerEventSerializer,
    EventOrderSerializer,
    EventSerializer,
)


class EventOrderViewSet(viewsets.ModelViewSet):
    permission_classes = [
        AllowCoordinator | AllowVendor | get_additional_permissions_write()
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
        user = self.request.user
        if user.user_type == get_user_model().Types.VENDOR:
            return EventOrder.objects.filter(
                school_group__activity_order__activity__originization=user.organization_member.organization
            ).order_by("-start_time")

        return EventOrder.objects.filter(
            school_group__activity_order__school=user.school_member.school
        ).order_by("-start_time")


class EventViewSet(viewsets.ModelViewSet):
    permission_classes = [
        AllowCoordinator | AllowInstructor | get_additional_permissions_write()
    ]
    serializer_class = EventSerializer
    lookup_field = "slug"
    filterset_fields = {
        "start_time": ["gte", "lte"],
        "has_summary": ["exact"],
        "is_canceled": ["exact"],
    }

    def get_queryset(self):
        user = self.request.user
        if user.user_type == get_user_model().Types.INSTRUCTOR:
            return Event.objects.filter(school_group__instructor=user).order_by(
                "-start_time"
            )

        return Event.objects.filter(
            school_group__activity_order__in=user.school_member.school.school_activity_orders.all()
        ).order_by("-start_time")


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
