from rest_framework import viewsets

from server.events.models import Event
from server.utils.permission_classes import AllowCoordinator

from .serializers import EventSerializer


class EventViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowCoordinator]
    serializer_class = EventSerializer

    queryset = Event.objects.all()
