from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from server.organizations.models import OrganizationMember
from server.schools.models import SchoolMember

from ..helpers import send_user_invite
from ..models import (
    Consumer,
    ConsumerProfile,
    Coordinator,
    CoordinatorProfile,
    Instructor,
    InstructorProfile,
    Supervisor,
    SupervisorProfile,
    Vendor,
    VendorProfile,
)

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["slug", "name", "email", "url", "user_type"]

        extra_kwargs = {
            "url": {"view_name": "api:user-detail", "lookup_field": "username"}
        }


class ConsumerProfileSerializer(serializers.ModelSerializer):
    slug = serializers.ReadOnlyField(source="user.slug")

    class Meta:
        model = ConsumerProfile
        fields = ["slug", "gender", "profile_picture"]


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


class InstructorProfileSerializer(serializers.ModelSerializer):
    slug = serializers.ReadOnlyField(source="user.slug")

    class Meta:
        model = InstructorProfile
        fields = ["slug", "gender", "profile_picture"]


class VendorProfileSerializer(serializers.ModelSerializer):
    slug = serializers.ReadOnlyField(source="user.slug")

    class Meta:
        model = VendorProfile
        fields = ["slug", "gender", "profile_picture", "phone_number"]


class ManageConsumersSerializer(serializers.ModelSerializer):
    profile = ConsumerProfileSerializer()

    class Meta:
        model = Consumer
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
        create user, update profile, attach to school, invite user via email
        """
        profile_data = validated_data.pop("profile", None)
        consumer = Consumer.objects.create(**validated_data)

        if profile_data:
            profile = ConsumerProfile.objects.get(user=consumer)
            for attr, value in profile_data.items():
                setattr(profile, attr, value)
            profile.save()

        SchoolMember.objects.create(
            user=consumer, school=self.context["request"].user.school_member.school
        )
        send_user_invite(validated_data["email"])
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
            send_user_invite(validated_data["email"])

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
        send_user_invite(validated_data["email"])
        return coordinator

    def update(self, instance, validated_data):
        has_email_changed = validated_data.get(
            "email"
        ) and instance.email != validated_data.get("email")

        instance.name = validated_data.get("name", instance.name)
        instance.email = validated_data.get("email", instance.email)
        instance.save()

        if has_email_changed:
            send_user_invite(validated_data["email"])

        return instance


class ManageSupervisorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supervisor
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
        supervisor = Supervisor.objects.create(**validated_data)

        SchoolMember.objects.create(
            user=supervisor, school=self.context["request"].user.school_member.school
        )
        send_user_invite(validated_data["email"])
        return supervisor

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.email = validated_data.get("email", instance.email)
        instance.save()

        if validated_data.get("email"):
            # invite again on email change
            send_user_invite(validated_data["email"])

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
        send_user_invite(validated_data["email"])
        return vendor

    def update(self, instance, validated_data):
        has_email_changed = validated_data.get(
            "email"
        ) and instance.email != validated_data.get("email")

        instance.name = validated_data.get("name", instance.name)
        instance.email = validated_data.get("email", instance.email)
        instance.save()

        if has_email_changed:
            send_user_invite(validated_data["email"])

        return instance


class ManageInstructorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instructor
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
        instructor = Instructor.objects.create(**validated_data)

        OrganizationMember.objects.create(
            user=instructor,
            organization=self.context["request"].user.organization_member.organization,
        )
        send_user_invite(validated_data["email"])
        return instructor

    def update(self, instance, validated_data):
        has_email_changed = validated_data.get(
            "email"
        ) and instance.email != validated_data.get("email")

        instance.name = validated_data.get("name", instance.name)
        instance.email = validated_data.get("email", instance.email)
        instance.save()

        if has_email_changed:
            send_user_invite(validated_data["email"])

        return instance
