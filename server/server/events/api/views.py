from rest_framework import viewsets

from server.events.models import Event
from server.utils.permission_classes import AllowCoordinator

from .serializers import EventSerializer


class EventViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowCoordinator]
    serializer_class = EventSerializer
    filterset_fields = {
        "start_time": ["gte", "lte"],
    }

    def get_queryset(self):
        return Event.objects.filter(
            school_group__activity_order__in=self.request.user.school_member.school.school_activity_orders.all()
        )
