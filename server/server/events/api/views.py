from django.contrib.auth import get_user_model
from rest_framework import viewsets

from server.events.models import Event
from server.utils.permission_classes import (
    AllowConsumerReadOnly,
    AllowCoordinator,
    AllowInstructor,
)

from .serializers import ConsumerEventSerializer, EventSerializer


class EventViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowCoordinator | AllowInstructor]
    serializer_class = EventSerializer
    lookup_field = "slug"
    filterset_fields = {"start_time": ["gte", "lte"], "has_summary": ["exact"]}

    def get_queryset(self):
        user = self.request.user
        if user.user_type == get_user_model().Types.INSTRUCTOR:
            return Event.objects.filter(school_group__instructor=user)

        return Event.objects.filter(
            school_group__activity_order__in=user.school_member.school.school_activity_orders.all()
        )


class ConsumerEventViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowConsumerReadOnly]
    serializer_class = ConsumerEventSerializer
    lookup_field = "slug"
    filterset_fields = {
        "start_time": ["gte", "lte"],
    }

    def get_queryset(self):
        return Event.objects.filter(school_group__consumers=self.request.user)
