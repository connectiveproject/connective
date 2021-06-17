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
    queryset = Event.objects.all()
