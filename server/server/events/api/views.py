from django.contrib.auth import get_user_model
from rest_framework import viewsets

from server.events.models import Event
from server.utils.permission_classes import AllowConsumerReadOnly, AllowCoordinator

from .serializers import EventSerializer


class EventViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowCoordinator | AllowConsumerReadOnly]
    serializer_class = EventSerializer
    filterset_fields = {
        "start_time": ["gte", "lte"],
    }

    def get_queryset(self):
        user = self.request.user
        if user.user_type == get_user_model().Types.CONSUMER:
            return Event.objects.filter(school_group__consumers=user)

        return Event.objects.filter(
            school_group__activity_order__in=user.school_member.school.school_activity_orders.all()
        )
