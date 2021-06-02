from django.conf import settings
from rest_framework.permissions import BasePermission


class AllowAllDebug(BasePermission):
    def has_permission(self, request, view):
        return settings.DEBUG
