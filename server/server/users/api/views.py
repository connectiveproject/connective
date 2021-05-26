from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from ..models import ConsumerProfile, CoordinatorProfile, VendorProfile
from .serializers import (
    ConsumerProfileSerializer,
    CoordinatorProfileSerializer,
    UserSerializer,
    VendorProfileSerializer,
)

User = get_user_model()


class UserViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = "username"

    def get_queryset(self, *args, **kwargs):
        return self.queryset.filter(id=self.request.user.id)

    @action(detail=False, methods=["GET"])
    def me(self, request):
        serializer = UserSerializer(request.user, context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)


class ConsumerProfileViewSet(ModelViewSet):
    serializer_class = ConsumerProfileSerializer
    queryset = ConsumerProfile.objects.all()

    @action(detail=False, methods=["GET"])
    def me(self, request):
        serializer = ConsumerProfileSerializer(
            request.user.consumerprofile, context={"request": request}
        )
        return Response(status=status.HTTP_200_OK, data=serializer.data)


class CoordinatorProfileViewSet(ModelViewSet):
    serializer_class = CoordinatorProfileSerializer
    queryset = CoordinatorProfile.objects.all()

    @action(detail=False, methods=["GET"])
    def me(self, request):
        serializer = CoordinatorProfileSerializer(
            request.user.coordinatorprofile, context={"request": request}
        )
        return Response(status=status.HTTP_200_OK, data=serializer.data)


class VendorProfileViewSet(ModelViewSet):
    serializer_class = VendorProfileSerializer
    queryset = VendorProfile.objects.all()

    @action(detail=False, methods=["GET"])
    def me(self, request):
        serializer = VendorProfileSerializer(
            request.user.vendorprofile, context={"request": request}
        )
        return Response(status=status.HTTP_200_OK, data=serializer.data)
