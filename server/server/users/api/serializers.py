from django.contrib.auth import get_user_model
from rest_framework import serializers

from server.schools.models import SchoolMember

from ..models import Consumer, ConsumerProfile, CoordinatorProfile, VendorProfile

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


class VendorProfileSerializer(serializers.ModelSerializer):
    slug = serializers.ReadOnlyField(source="user.slug")

    class Meta:
        model = VendorProfile
        fields = ["slug", "gender", "profile_picture", "phone_number"]


class ManageConsumersSerializer(serializers.ModelSerializer):
    profile = ConsumerProfileSerializer()

    class Meta:
        model = Consumer
        fields = ["name", "email", "profile"]

    def create(self, validated_data):
        profile_data = validated_data.pop("profile")
        consumer = Consumer(**validated_data)
        consumer._no_profile_create = True
        consumer.save()

        ConsumerProfile.objects.create(user=consumer, **profile_data)
        SchoolMember.objects.create(
            user=consumer, school=self.context["request"].user.school_member.school
        )
        return consumer
