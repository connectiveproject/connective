# The following import is needed to allow to annotate the return value of UserFileParser from withih the class.
# see here: https://stackoverflow.com/questions/15853469/putting-current-class-as-return-type-annotation
from __future__ import annotations

import csv
import io
import logging
import os
from datetime import datetime

from allauth.account.utils import url_str_to_user_pk as uid_decoder
from dj_rest_auth.views import LoginView, PasswordResetConfirmView
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils import timezone
from django.utils.encoding import force_text
from django_filters.rest_framework import DjangoFilterBackend
from pandas import ExcelFile
from rest_framework import filters, status
from rest_framework.decorators import action, authentication_classes
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from server.termsofuse.models import TermsOfUseDocument
from server.users.api_helpers import (
    PrivilegeAccessMixin,
    get_privilege_permission_classes,
)
from server.users.helpers import is_recaptcha_token_valid, send_password_recovery
from server.users.models import (
    BaseProfile,
    Consumer,
    ConsumerProfile,
    Coordinator,
    CoordinatorProfile,
    Instructor,
    InstructorProfile,
    Notification,
    SupervisorProfile,
    Vendor,
    VendorProfile,
)
from server.users.notifications import NOTIFICATIONS_RETENTION_DAYS
from server.utils.analytics_utils import event, identify_track
from server.utils.db_utils import get_additional_permissions_write
from server.utils.factories import get_user_utils
from server.utils.permission_classes import (
    AllowAuthenticatedReadOnly,
    AllowConsumer,
    AllowCoordinator,
    AllowInstructor,
    AllowSupervisor,
    AllowVendor,
)
from server.utils.privileges import (
    PRIV_USER_CONSUMER_EDIT,
    PRIV_USER_CONSUMER_VIEW,
    PRIV_USER_INSTRUCTOR_EDIT,
    PRIV_USER_INSTRUCTOR_VIEW,
)

from .renderers import UsersCSVRenderer
from .serializers import (
    ConsumerProfileSerializer,
    CoordinatorProfileSerializer,
    CurrentUserSerializer,
    InstructorProfileSerializer,
    ManageConsumersSerializer,
    ManageCoordinatorsSerializer,
    ManageInstructorsSerializer,
    ManageVendorsSerializer,
    NotificationsSerializer,
    SupervisorProfileSerializer,
    UserProfileSerializer,
    UserSerializer,
    VendorProfileSerializer,
)

logger = logging.getLogger(__name__)

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
        user = User.objects.get(pk=pk)
        identify_track(user, event.INITIAL_PASSWORD_CREATED)
        return Response({"email": user.email})


@authentication_classes(settings.BASE_REST_AUTHENTICATION_CLASSES)
class LoginView(LoginView):
    """add analytics functionality"""

    def login(self):
        super().login()
        user = self.user
        identify_track(user, event.APP_LOGIN)


class UserViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = "username"

    def get_queryset(self, *args, **kwargs):
        return self.queryset.filter(id=self.request.user.id)

    @action(detail=False, methods=["GET"])
    def me(self, request):
        serializer = CurrentUserSerializer(request.user, context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    @action(detail=False, methods=["POST"], permission_classes=[AllowAny])
    def recover_password(self, request):
        """
        send password recovery email if requested email exists
        """
        token = request.data.get("recaptcha_token", None)
        if not is_recaptcha_token_valid(token, request):
            return Response(
                data={"error": "ReCAPTCHA could not be verified"},
                status=status.HTTP_406_NOT_ACCEPTABLE,
            )

        email = request.data.get("email", None)
        if not email:
            return Response(
                {"email": ["email must be specified"]},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if User.objects.filter(email=email).exists():
            send_password_recovery(email)
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(
            {"email": ["email does not exist"]},
            status=status.HTTP_400_BAD_REQUEST,
        )

    @action(detail=False, methods=["PATCH"], permission_classes=[IsAuthenticated])
    def accept_terms_of_use(self, request):
        TermsOfUseDocument.objects.sign(request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ConsumerProfileViewSet(ModelViewSet):
    permission_classes = [AllowConsumer | get_additional_permissions_write()]
    serializer_class = ConsumerProfileSerializer

    def get_queryset(self):
        return ConsumerProfile.objects.filter(user=self.request.user)

    lookup_field = "user__slug"

    @action(detail=False, methods=["GET"])
    def me(self, request):
        serializer = ConsumerProfileSerializer(
            request.user.consumerprofile, context={"request": request}
        )
        return Response(status=status.HTTP_200_OK, data=serializer.data)


class UserProfileViewSet(ModelViewSet):
    permission_classes = [
        AllowAuthenticatedReadOnly | get_additional_permissions_write()
    ]
    serializer_class = UserProfileSerializer

    lookup_field = "user__slug"

    def get_queryset(self):
        return get_user_utils().get_user_profile(self.request.user)

    @action(detail=False, methods=["GET"])
    def me(self, request):
        profile: BaseProfile = get_user_utils().get_user_profile(request.user)
        serializer = UserProfileSerializer(
            profile,
            context={"request": request},
        )
        return Response(status=status.HTTP_200_OK, data=serializer.data)


class CoordinatorProfileViewSet(ModelViewSet):
    permission_classes = [AllowCoordinator | get_additional_permissions_write()]
    serializer_class = CoordinatorProfileSerializer
    queryset = CoordinatorProfile.objects.all()
    lookup_field = "user__slug"

    @action(detail=False, methods=["GET"])
    def me(self, request):
        profile: BaseProfile = get_user_utils().get_user_profile(request.user)
        serializer = CoordinatorProfileSerializer(
            profile,
            context={"request": request},
        )
        return Response(status=status.HTTP_200_OK, data=serializer.data)


class InstructorProfileViewSet(ModelViewSet):
    permission_classes = [AllowInstructor | get_additional_permissions_write()]
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
    permission_classes = [AllowVendor | get_additional_permissions_write()]
    serializer_class = VendorProfileSerializer
    queryset = VendorProfile.objects.all()
    lookup_field = "user__slug"

    @action(detail=False, methods=["GET"])
    def me(self, request):
        profile: BaseProfile = get_user_utils().get_user_profile(request.user)
        serializer = VendorProfileSerializer(profile, context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)


class SupervisorProfileViewSet(ModelViewSet):
    permission_classes = [AllowSupervisor | get_additional_permissions_write()]
    serializer_class = SupervisorProfileSerializer
    queryset = SupervisorProfile.objects.all()
    lookup_field = "user__slug"

    @action(detail=False, methods=["GET"])
    def me(self, request):
        serializer = SupervisorProfileSerializer(
            request.user.supervisorprofile, context={"request": request}
        )
        return Response(status=status.HTTP_200_OK, data=serializer.data)


class ManageConsumersViewSet(ModelViewSet, PrivilegeAccessMixin):
    privileges_read = [PRIV_USER_CONSUMER_VIEW]
    privileges_write = [PRIV_USER_CONSUMER_EDIT]

    permission_classes = [
        get_additional_permissions_write()
        | get_privilege_permission_classes(privileges_read, privileges_write)
    ]
    serializer_class = ManageConsumersSerializer
    lookup_field = "slug"
    search_fields = ["email", "name"]
    filter_backends = (
        filters.SearchFilter,
        filters.OrderingFilter,
        DjangoFilterBackend,
    )
    filterset_fields = ["consumerprofile__grade"]

    def get_queryset(self):
        queryset = Consumer.objects.all().order_by("email")
        my_school_only: bool = self.request.query_params.get("my_school_only", False)
        if my_school_only:
            return queryset.filter(
                school_member__school=self.request.user.school_member.school
            )
        if self.is_admin_scope(self.request):
            return queryset
        schools = self.get_allowed_schools(self.request)
        return queryset.filter(school_member__school__in=schools)

    @action(detail=False, methods=["POST"])
    def bulk_create(self, request):
        users_to_invite = []
        if not request.FILES:
            return Response("File must be included", status=status.HTTP_400_BAD_REQUEST)

        request_file = request.FILES["file"]
        parser: UserFileParser = UserFileParser.create_user_file_parser(
            request_file, True
        )
        errors = parser.get_errors()
        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

        users_from_file = parser.get_user_list()

        already_existing_emails = User.objects.filter(
            email__in=[user["email"].lower() for user in users_from_file]
        ).values_list("email", flat=True)
        users_to_invite = [
            user
            for user in users_from_file
            if user["email"].lower() not in already_existing_emails
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
    permission_classes = [AllowCoordinator | get_additional_permissions_write()]
    serializer_class = ManageCoordinatorsSerializer
    lookup_field = "slug"
    search_fields = ["email", "name"]
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)

    def get_queryset(self):
        return Coordinator.objects.filter(
            school_member__school=self.request.user.school_member.school
        ).order_by("email")

    @action(detail=False, methods=["POST"])
    def bulk_create(self, request):
        users_to_invite = []
        if not request.FILES:
            return Response("File must be included", status=status.HTTP_400_BAD_REQUEST)

        request_file = request.FILES["file"]
        parser: UserFileParser = UserFileParser.create_user_file_parser(
            request_file, True
        )
        errors = parser.get_errors()
        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

        users_from_file = parser.get_user_list()

        already_existing_emails = User.objects.filter(
            email__in=[user["email"] for user in users_from_file]
        ).values_list("email", flat=True)
        users_to_invite = [
            user
            for user in users_from_file
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


class ExportConsumerListViewSet(ModelViewSet, PrivilegeAccessMixin):
    privileges_read = [PRIV_USER_CONSUMER_VIEW]
    privileges_write = [PRIV_USER_CONSUMER_EDIT]
    permission_classes = [
        get_additional_permissions_write()
        | get_privilege_permission_classes(privileges_read, privileges_write)
    ]

    serializer_class = ManageConsumersSerializer
    lookup_field = "slug"
    renderer_classes = (UsersCSVRenderer,)
    search_fields = ["email", "name"]
    filter_backends = (
        filters.SearchFilter,
        filters.OrderingFilter,
        DjangoFilterBackend,
    )
    filterset_fields = ["consumerprofile__grade"]

    def get_queryset(self):
        queryset = Consumer.objects.all()
        my_school_only: bool = self.request.query_params.get("my_school_only", False)
        if my_school_only:
            return queryset.filter(
                school_member__school=self.request.user.school_member.school
            )
        if self.is_admin_scope(self.request):
            return queryset
        schools = self.get_allowed_schools(self.request)
        return queryset.filter(school_member__school__in=schools)


class ExportCoordinatorListViewSet(ModelViewSet):
    permission_classes = [AllowCoordinator | get_additional_permissions_write()]
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
    permission_classes = [AllowVendor | get_additional_permissions_write()]
    serializer_class = ManageVendorsSerializer
    lookup_field = "slug"
    search_fields = ["email", "name"]
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)

    def get_queryset(self):
        return Vendor.objects.filter(
            organization_member__organization=self.request.user.organization_member.organization
        )


class ManageInstructorsViewSet(ModelViewSet, PrivilegeAccessMixin):
    privileges_read = [PRIV_USER_INSTRUCTOR_VIEW]
    privileges_write = [PRIV_USER_INSTRUCTOR_EDIT]

    permission_classes = [
        get_additional_permissions_write()
        | get_privilege_permission_classes(privileges_read, privileges_write)
    ]

    serializer_class = ManageInstructorsSerializer
    lookup_field = "slug"
    search_fields = ["email", "name"]
    filter_backends = (
        filters.SearchFilter,
        filters.OrderingFilter,
        DjangoFilterBackend,
    )
    filterset_fields = ["organization_member__organization"]

    def get_queryset(self):
        if self.is_admin_scope(self.request):
            return Instructor.objects.all()
        return Instructor.objects.filter(
            organization_member__organization__in=self.get_allowed_organizations(
                self.request
            )
        )


class MyNotificationsViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = NotificationsSerializer
    lookup_field = "slug"
    search_fields = ["created_at", "status"]

    def get_queryset(self):
        oldest_date: datetime = timezone.now() - timezone.timedelta(
            days=NOTIFICATIONS_RETENTION_DAYS
        )
        return (
            Notification.objects.filter(user=self.request.user)
            .filter(created_at__gt=oldest_date)
            .filter(status__in=[Notification.Status.NEW, Notification.Status.READ])
            .order_by("-created_at")
        )

    @action(detail=False, methods=["GET"])
    def has_new(self, request):
        result: bool = (
            self.get_queryset().filter(status=Notification.Status.NEW).exists()
        )
        return Response(status=status.HTTP_200_OK, data=result)

    @action(detail=False, methods=["POST"])
    def mark_all_as_read(self, request):
        max_slug = request.data.get("max_slug")
        if not max_slug:
            return Response(
                "max slug to update is required", status=status.HTTP_400_BAD_REQUEST
            )
        max_notification: Notification = self.get_queryset().get(slug=max_slug)
        self.get_queryset().filter(status="NEW").filter(
            created_at__lte=max_notification.created_at
        ).update(status="READ")
        serializer = NotificationsSerializer(self.get_queryset(), many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)


class UserFileParser:

    name_mandatory: bool = True

    def __init__(self, file, name_mandatory: bool):
        self.file = file
        self.errors = []
        self.email_set = set()
        self.name_mandatory = name_mandatory
        self.parse()

    def get_reader(self):
        logger.error("Not implemented. Need to use sub-class")
        return "Not implemented"

    def get_user_list(self):
        return self.user_dict_list

    def validate_email_format(mail: str) -> bool:
        try:
            validate_email(mail)
            return True
        except ValidationError:
            return False

    def parse(self):
        self.user_dict_list = []
        row_index: int = 1
        found_email_column: bool = False
        for row in self.get_reader():
            row_index += 1
            if row_index > settings.FILE_UPLOAD_MAX_ROWS:
                self.errors.append(
                    {"row": -1, "error": "invite.maxRowsPerFileExceeded"}
                )
                break
            name = row.get("name").strip() if row.get("name") else ""
            email = row.get("email").strip().lower() if row.get("email") else ""
            if email:
                found_email_column = True
            elif not found_email_column:
                self.errors.append({"row": -1, "error": "invite.missingEmailColumn"})
                break
            gender = (
                row.get("gender").strip().upper()
                if row.get("gender")
                else ConsumerProfile.Gender.UNKNOWN
            )
            grade = row.get("grade").strip().upper() if row.get("grade") else ""
            if self.name_mandatory and not name:
                self.errors.append(
                    {"row": row_index, "error": "invite.nameFieldIsRequired"}
                )
            elif not email or not UserFileParser.validate_email_format(email):
                self.errors.append(
                    {"row": row_index, "error": "invite.emailFieldIsInvalid"}
                )
            elif email in self.email_set:
                self.errors.append(
                    {"row": row_index, "error": "invite.sameEmailAppearMoreThanOnce"}
                )
            else:
                self.user_dict_list.append(
                    {
                        "name": name,
                        "email": email,
                        "profile": {"gender": gender, "grade": grade},
                    }
                )
                self.email_set.add(email)

    def get_errors(self):
        return self.errors

    def create_user_file_parser(file, name_mandatory: bool) -> UserFileParser:
        _, file_extension = os.path.splitext(file.name)
        if file_extension == ".csv":
            return CSVFileParser(file, name_mandatory)
        if file_extension == ".xls" or file_extension == ".xlsx":
            return ExcelFileParser(file, name_mandatory)
        raise Exception(f"Unsupported file type: {file_extension}")


class CSVFileParser(UserFileParser):
    def __init__(self, file, name_mandatory: bool):
        super().__init__(file, name_mandatory)

    def get_reader(self):
        try:
            return csv.DictReader(
                io.StringIO(self.file.read().decode(encoding="utf-8-sig"), newline=None)
            )
        except UnicodeDecodeError as err:
            self.errors.append({"row": -1, "error": "invite.uploadFileErrorUnicode"})
            logger.error("Upload file error", err)
            return []


class ExcelFileParser(UserFileParser):
    def __init__(self, file, name_mandatory: bool):
        super().__init__(file, name_mandatory)

    def get_reader(self):
        xls = ExcelFile(self.file)
        df = xls.parse(xls.sheet_names[0])
        return df.to_dict("records")
