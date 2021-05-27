from django.contrib.auth import get_user_model
from rest_framework import serializers

from ..models import ConsumerProfile, CoordinatorProfile, VendorProfile

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "name", "email", "url", "user_type"]

        extra_kwargs = {
            "url": {"view_name": "api:user-detail", "lookup_field": "username"}
        }


class ConsumerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsumerProfile
        exclude = ("user",)


class CoordinatorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoordinatorProfile
        exclude = ("user",)


class VendorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorProfile
        exclude = ("user",)
