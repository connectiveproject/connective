import csv
import io
import os

from allauth.account.utils import url_str_to_user_pk as uid_decoder
from dj_rest_auth.views import PasswordResetConfirmView
from django.contrib.auth import get_user_model
from django.utils.encoding import force_text
from rest_framework import filters, status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from server.utils.permission_classes import (
    AllowConsumer,
    AllowCoordinator,
    AllowInstructor,
    AllowVendor,
)

from ..models import (
    Consumer,
    ConsumerProfile,
    Coordinator,
    CoordinatorProfile,
    Instructor,
    InstructorProfile,
    Vendor,
    VendorProfile,
)
from .renderers import UsersCSVRenderer
from .serializers import (
    ConsumerProfileSerializer,
    CoordinatorProfileSerializer,
    InstructorProfileSerializer,
    ManageConsumersSerializer,
    ManageCoordinatorsSerializer,
    ManageInstructorsSerializer,
    ManageVendorsSerializer,
    UserSerializer,
    VendorProfileSerializer,
)

User = get_user_model()


class PassResetConfirmView(PasswordResetConfirmView):
    """
    return the email to the client after password reset
    """

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # get and return the correlating email address
        pk = force_text(uid_decoder(request.data["uid"]))
        email = User.objects.get(pk=pk).email
        return Response({"email": email})


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
    permission_classes = [AllowConsumer]
    serializer_class = ConsumerProfileSerializer
    queryset = ConsumerProfile.objects.all()
    lookup_field = "user__slug"

    @action(detail=False, methods=["GET"])
    def me(self, request):
        serializer = ConsumerProfileSerializer(
            request.user.consumerprofile, context={"request": request}
        )
        return Response(status=status.HTTP_200_OK, data=serializer.data)


class CoordinatorProfileViewSet(ModelViewSet):
    permission_classes = [AllowCoordinator]
    serializer_class = CoordinatorProfileSerializer
    queryset = CoordinatorProfile.objects.all()
    lookup_field = "user__slug"

    @action(detail=False, methods=["GET"])
    def me(self, request):
        serializer = CoordinatorProfileSerializer(
            request.user.coordinatorprofile, context={"request": request}
        )
        return Response(status=status.HTTP_200_OK, data=serializer.data)


class InstructorProfileViewSet(ModelViewSet):
    permission_classes = [AllowInstructor]
    serializer_class = InstructorProfileSerializer
    queryset = InstructorProfile.objects.all()
    lookup_field = "user__slug"

    @action(detail=False, methods=["GET"])
    def me(self, request):
        serializer = InstructorProfileSerializer(
            request.user.instructorprofile, context={"request": request}
        )
        return Response(status=status.HTTP_200_OK, data=serializer.data)


class VendorProfileViewSet(ModelViewSet):
    permission_classes = [AllowVendor]
    serializer_class = VendorProfileSerializer
    queryset = VendorProfile.objects.all()
    lookup_field = "user__slug"

    @action(detail=False, methods=["GET"])
    def me(self, request):
        serializer = VendorProfileSerializer(
            request.user.vendorprofile, context={"request": request}
        )
        return Response(status=status.HTTP_200_OK, data=serializer.data)


class ManageConsumersViewSet(ModelViewSet):
    permission_classes = [AllowCoordinator]
    serializer_class = ManageConsumersSerializer
    lookup_field = "slug"
    search_fields = ["email", "name"]
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)

    def get_queryset(self):
        return Consumer.objects.filter(
            school_member__school=self.request.user.school_member.school
        )

    @action(detail=False, methods=["POST"])
    def bulk_create(self, request):
        users_to_invite = []
        if not request.FILES:
            return Response("File must be included", status=status.HTTP_400_BAD_REQUEST)

        request_file = request.FILES["file"]
        _, file_extension = os.path.splitext(request_file.name)
        if file_extension != ".csv":
            return Response("Unsupported file type", status=status.HTTP_400_BAD_REQUEST)

        emails = set()
        for row in csv.DictReader(
            io.StringIO(request_file.read().decode(encoding="utf-8-sig"))
        ):
            name = row.get("name").strip() if row.get("name") else ""
            email = row.get("email").strip() if row.get("email") else ""
            gender = (
                row.get("gender").strip()
                if row.get("gender")
                else ConsumerProfile.Gender.UNKNOWN
            )
            if email not in emails:
                emails.add(email)
                users_to_invite.append(
                    {
                        "name": name,
                        "email": email,
                        "profile": {"gender": gender},
                    }
                )

        already_existing_emails = User.objects.filter(
            email__in=[user["email"] for user in users_to_invite]
        ).values_list("email", flat=True)
        users_to_invite = [
            user
            for user in users_to_invite
            if user["email"] not in already_existing_emails
        ]

        serializer = ManageConsumersSerializer(
            data=users_to_invite,
            context={"request": request},
            many=True,
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ManageCoordinatorsViewSet(ModelViewSet):
    permission_classes = [AllowCoordinator]
    serializer_class = ManageCoordinatorsSerializer
    lookup_field = "slug"
    search_fields = ["email", "name"]
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)

    def get_queryset(self):
        return Coordinator.objects.filter(
            school_member__school=self.request.user.school_member.school
        )

    @action(detail=False, methods=["POST"])
    def bulk_create(self, request):
        users_to_invite = []
        if not request.FILES:
            return Response("File must be included", status=status.HTTP_400_BAD_REQUEST)

        request_file = request.FILES["file"]
        _, file_extension = os.path.splitext(request_file.name)
        if file_extension != ".csv":
            return Response("Unsupported file type", status=status.HTTP_400_BAD_REQUEST)

        emails = set()
        for row in csv.DictReader(
            io.StringIO(request_file.read().decode(encoding="utf-8-sig"))
        ):
            name = row.get("name").strip() if row.get("name") else ""
            email = row.get("email").strip() if row.get("email") else ""
            if email not in emails:
                # add user if email not seem already in the file
                users_to_invite.append(
                    {
                        "name": name,
                        "email": email,
                    }
                )
                emails.add(email)

        # remove already existing emails
        already_existing_emails = User.objects.filter(
            email__in=[user["email"] for user in users_to_invite]
        ).values_list("email", flat=True)
        users_to_invite = [
            user
            for user in users_to_invite
            if user["email"] not in already_existing_emails
        ]

        serializer = ManageCoordinatorsSerializer(
            data=users_to_invite,
            context={"request": request},
            many=True,
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ExportConsumerListViewSet(ModelViewSet):
    permission_classes = [AllowCoordinator]
    serializer_class = ManageConsumersSerializer
    lookup_field = "slug"
    renderer_classes = (UsersCSVRenderer,)
    search_fields = ["email", "name"]
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)

    def get_queryset(self):
        return Consumer.objects.filter(
            school_member__school=self.request.user.school_member.school
        )


class ExportCoordinatorListViewSet(ModelViewSet):
    permission_classes = [AllowCoordinator]
    serializer_class = ManageCoordinatorsSerializer
    lookup_field = "slug"
    renderer_classes = (UsersCSVRenderer,)
    search_fields = ["email", "name"]
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)

    def get_queryset(self):
        return Coordinator.objects.filter(
            school_member__school=self.request.user.school_member.school
        )


class ManageVendorsViewSet(ModelViewSet):
    permission_classes = [AllowVendor]
    serializer_class = ManageVendorsSerializer
    lookup_field = "slug"
    search_fields = ["email", "name"]
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)

    def get_queryset(self):
        return Vendor.objects.filter(
            organization_member__organization=self.request.user.organization_member.organization
        )


class ManageInstructorsViewSet(ModelViewSet):
    permission_classes = [AllowVendor]
    serializer_class = ManageInstructorsSerializer
    lookup_field = "slug"
    search_fields = ["email", "name"]
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)

    def get_queryset(self):
        return Instructor.objects.filter(
            organization_member__organization=self.request.user.organization_member.organization
        )
