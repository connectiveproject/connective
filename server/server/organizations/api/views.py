from rest_framework import mixins, viewsets

from server.organizations.models import Activity, ActivityMedia, Organization

from .serializers import (
    ActivityMediaSerializer,
    ActivitySerializer,
    OrganizationSerializer,
)


class OrganizationViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    mixins.GenericViewSet,
):
    serializer_class = OrganizationSerializer
    lookup_field = "slug"

    def get_queryset(self):
        return Organization.objects.filter(
            organization_member__in=[self.request.user.organization_member]
        )


class ActivityViewSet(viewsets.ModelViewSet):
    serializer_class = ActivitySerializer
    lookup_field = "slug"

    queryset = Activity.objects.all()


class ActivityMediaViewSet(viewsets.ModelViewSet):
    serializer_class = ActivityMediaSerializer
    lookup_field = "slug"
    queryset = ActivityMedia.objects.all()
