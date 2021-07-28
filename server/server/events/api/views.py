from datetime import datetime, timedelta

from django.contrib.auth import get_user_model
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from server.events.models import ConsumerEventFeedback, Event
from server.utils.permission_classes import (
    AllowConsumer,
    AllowConsumerReadOnly,
    AllowCoordinator,
    AllowInstructor,
)

from .serializers import (
    ConsumerEventFeedbackSerializer,
    ConsumerEventSerializer,
    EventSerializer,
)


class EventViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowCoordinator | AllowInstructor]
    serializer_class = EventSerializer
    lookup_field = "slug"
    filterset_fields = {"start_time": ["gte", "lte"], "has_summary": ["exact"]}

    def get_queryset(self):
        user = self.request.user
        if user.user_type == get_user_model().Types.INSTRUCTOR:
            return Event.objects.filter(school_group__instructor=user).order_by(
                "-start_time"
            )

        return Event.objects.filter(
            school_group__activity_order__in=user.school_member.school.school_activity_orders.all()
        ).order_by("-start_time")

    @action(detail=False, methods=["POST"])
    def recurring_events_create(self, request):
        recurrence = request.data.pop("recurrence", None)
        if recurrence != "weekly":
            return Response(
                "received invalid event 'recurrence'",
                status=status.HTTP_400_BAD_REQUEST,
            )
        events = []
        base_start_time = datetime.strptime(
            request.data.pop("start_time", None), "%Y-%m-%d %H:%M"
        )
        base_end_time = datetime.strptime(
            request.data.pop("end_time", None), "%Y-%m-%d %H:%M"
        )
        if not base_start_time or not base_end_time:
            return Response(
                "received invalid start/end time", status=status.HTTP_400_BAD_REQUEST
            )

        for i in range(0, 54):
            start_time = datetime.strftime(
                base_start_time + timedelta(days=i * 7), "%Y-%m-%d %H:%M"
            )
            end_time = datetime.strftime(
                base_end_time + timedelta(days=i * 7), "%Y-%m-%d %H:%M"
            )
            events.append(
                {**request.data, "start_time": start_time, "end_time": end_time}
            )

        serializer = EventSerializer(
            data=events,
            many=True,
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ConsumerEventViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowConsumerReadOnly]
    serializer_class = ConsumerEventSerializer
    lookup_field = "slug"
    filterset_fields = {
        "start_time": ["gte", "lte"],
    }

    def get_queryset(self):
        return Event.objects.filter(school_group__consumers=self.request.user)


class ConsumerEventFeedbackViewset(viewsets.ModelViewSet):
    permission_classes = [AllowConsumer]
    serializer_class = ConsumerEventFeedbackSerializer
    lookup_field = "slug"

    def get_queryset(self):
        return ConsumerEventFeedback.objects.filter(consumer=self.request.user)

    def perform_create(self, serializer):
        serializer.save(consumer=self.request.user)

    def perform_update(self, serializer):
        serializer.save(consumer=self.request.user)
