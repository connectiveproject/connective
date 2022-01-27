# from django.shortcuts import render
from rest_framework import filters
from rest_framework.viewsets import ModelViewSet

from server.connective_tags.models import ConnectiveTag
from server.connective_tags.serializers import TagsSerializer
from server.utils.permission_classes import AllowAuthenticatedReadOnly


class TagsViewSet(ModelViewSet):
    permission_classes = [AllowAuthenticatedReadOnly]
    serializer_class = TagsSerializer
    lookup_field = "slug"
    search_fields = ["slug"]
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)

    def get_queryset(self):
        return ConnectiveTag.objects.all()
