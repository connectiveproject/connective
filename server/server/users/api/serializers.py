from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from server.organizations.models import OrganizationMember
from server.schools.models import SchoolMember
from server.users.models import (
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
from server.users.notifications import NotificationRegistry, get_notification_registry

from ..helpers import send_user_invite

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    school_name = serializers.CharField(
        source="school_member.school.name", read_only=True
    )

    class Meta:
        model = User
        fields = [
            "slug",
            "name",
            "email",
            "url",
            "user_type",
            "is_signup_complete",
            "school_name",
        ]
        read_only_fields = ["slug", "url", "user_type", "school_name"]

        extra_kwargs = {
            "url": {"view_name": "api:user-detail", "lookup_field": "username"}
        }


class CurrentUserSerializer(UserSerializer):

    privileges = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "slug",
            "name",
            "email",
            "url",
            "user_type",
            "is_signup_complete",
            "school_name",
            "privileges",
        ]
        read_only_fields = [
            "slug",
            "url",
            "user_type",
            "school_name",
            "roles",
            "privileges",
        ]

        extra_kwargs = {
            "url": {"view_name": "api:user-detail", "lookup_field": "username"}
        }

    def get_privileges(self, obj):
        return list(obj.get_privilege_scopes().keys())


class ConsumerProfileSerializer(serializers.ModelSerializer):
    slug = serializers.ReadOnlyField(source="user.slug")

    class Meta:
        model = ConsumerProfile
        fields = ["slug", "gender", "grade", "profile_picture", "phone_number"]


class CoordinatorProfileSerializer(serializers.ModelSerializer):
    slug = serializers.ReadOnlyField(source="user.slug")

    class Meta:
        model = CoordinatorProfile
        fields = [
            "slug",
            "gender",
            "profile_picture",
            "job_description",
            "phone_number",
        ]


class InstructorProfileSerializer(serializers.ModelSerializer):
    slug = serializers.ReadOnlyField(source="user.slug")

    class Meta:
        model = InstructorProfile
        fields = ["slug", "gender", "profile_picture", "phone_number"]


class VendorProfileSerializer(serializers.ModelSerializer):
    slug = serializers.ReadOnlyField(source="user.slug")

    class Meta:
        model = VendorProfile
        fields = ["slug", "gender", "profile_picture", "phone_number"]


class SupervisorProfileSerializer(serializers.ModelSerializer):
    slug = serializers.ReadOnlyField(source="user.slug")

    class Meta:
        model = SupervisorProfile
        fields = [
            "slug",
            "gender",
            "profile_picture",
            "job_description",
            "phone_number",
        ]


class ManageConsumersSerializer(serializers.ModelSerializer):
    profile = ConsumerProfileSerializer()
    school_name = serializers.CharField(
        source="school_member.school.name", read_only=True
    )

    class Meta:
        model = Consumer
        fields = [
            "slug",
            "name",
            "email",
            "profile",
            "school_name",
        ]
        read_only_fields = ["school_name"]
        extra_kwargs = {
            "email": {
                "validators": [
                    UniqueValidator(queryset=User.objects.all(), lookup="iexact")
                ]
            },
        }

    def create(self, validated_data):
        """
        create user, update profile, attach to school, invite user via email
        """
        profile_data = validated_data.pop("profile", None)
        consumer = Consumer.objects.create(**validated_data)

        if profile_data:
            profile = consumer.profile
            for attr, value in profile_data.items():
                setattr(profile, attr, value)
            profile.save()

        SchoolMember.objects.create(
            user=consumer, school=self.context["request"].user.school_member.school
        )
        send_user_invite(consumer)
        return consumer

    def update(self, instance, validated_data):
        """
        update user & profile
        """
        has_email_changed = validated_data.get(
            "email"
        ) and instance.email != validated_data.get("email")

        instance.name = validated_data.get("name", instance.name)
        instance.email = validated_data.get("email", instance.email)

        profile_data = validated_data.pop("profile", None)
        if profile_data:
            profile = instance.profile
            for attr, value in profile_data.items():
                setattr(profile, attr, value)
            profile.save()

        instance.save()
        if has_email_changed:
            send_user_invite(instance)

        return instance


class ManageCoordinatorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coordinator
        fields = ["slug", "name", "email"]
        extra_kwargs = {
            "email": {
                "validators": [
                    UniqueValidator(queryset=User.objects.all(), lookup="iexact")
                ]
            },
        }

    def create(self, validated_data):
        """
        create user, attach to school, invite user via email
        """
        coordinator = Coordinator.objects.create(**validated_data)

        SchoolMember.objects.create(
            user=coordinator, school=self.context["request"].user.school_member.school
        )
        send_user_invite(coordinator)
        return coordinator

    def update(self, instance, validated_data):
        has_email_changed = validated_data.get(
            "email"
        ) and instance.email != validated_data.get("email")

        instance.name = validated_data.get("name", instance.name)
        instance.email = validated_data.get("email", instance.email)
        instance.save()

        if has_email_changed:
            send_user_invite(instance)

        return instance


class ManageVendorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ["slug", "name", "email"]
        extra_kwargs = {
            "email": {
                "validators": [
                    UniqueValidator(queryset=User.objects.all(), lookup="iexact")
                ]
            },
        }

    def create(self, validated_data):
        """
        create user, attach to org, invite user via email
        """
        vendor = Vendor.objects.create(**validated_data)

        OrganizationMember.objects.create(
            user=vendor,
            organization=self.context["request"].user.organization_member.organization,
        )
        send_user_invite(vendor)
        return vendor

    def update(self, instance, validated_data):
        has_email_changed = validated_data.get(
            "email"
        ) and instance.email != validated_data.get("email")

        instance.name = validated_data.get("name", instance.name)
        instance.email = validated_data.get("email", instance.email)
        instance.save()

        if has_email_changed:
            send_user_invite(instance)

        return instance


class ManageInstructorsSerializer(serializers.ModelSerializer):
    profile = InstructorProfileSerializer()

    class Meta:
        model = Instructor
        fields = ["slug", "name", "email", "profile"]
        extra_kwargs = {
            "email": {
                "validators": [
                    UniqueValidator(queryset=User.objects.all(), lookup="iexact")
                ]
            },
        }

    def create(self, validated_data):
        """
        create user, attach to org, invite user via email
        """
        profile_data = validated_data.pop("profile", None)
        instructor = Instructor.objects.create(**validated_data)

        if profile_data:
            profile = InstructorProfile.objects.get(user=instructor)
            for attr, value in profile_data.items():
                setattr(profile, attr, value)
            profile.save()

        OrganizationMember.objects.create(
            user=instructor,
            organization=self.context["request"].user.organization_member.organization,
        )
        send_user_invite(instructor)
        return instructor

    def update(self, instance, validated_data):
        has_email_changed = validated_data.get(
            "email"
        ) and instance.email != validated_data.get("email")

        instance.name = validated_data.get("name", instance.name)
        instance.email = validated_data.get("email", instance.email)

        profile_data = validated_data.pop("profile", None)
        if profile_data:
            profile = instance.profile
            for attr, value in profile_data.items():
                setattr(profile, attr, value)
            profile.save()

        instance.save()

        if has_email_changed:
            send_user_invite(instance)

        return instance


class NotificationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = [
            "slug",
            "created_at",
            "parameters",
            "status",
            "title_label",
            "action_label",
            "link",
            "link_parameters",
        ]

    title_label = serializers.SerializerMethodField(read_only=True)
    action_label = serializers.SerializerMethodField(read_only=True)
    link = serializers.SerializerMethodField(read_only=True)
    link_parameters = serializers.SerializerMethodField(read_only=True)

    def get_title_label(self, notification: Notification):
        registry: NotificationRegistry = get_notification_registry(
            notification.notification_code
        )
        return registry.title_label

    def get_action_label(self, notification: Notification):
        registry: NotificationRegistry = get_notification_registry(
            notification.notification_code
        )
        return registry.action_label

    def get_link(self, notification: Notification):
        registry: NotificationRegistry = get_notification_registry(
            notification.notification_code
        )
        return registry.link

    def get_link_parameters(self, notification: Notification):
        registry: NotificationRegistry = get_notification_registry(
            notification.notification_code
        )
        return registry.link_parameters
