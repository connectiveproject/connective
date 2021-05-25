from rest_framework import serializers

from server.organizations.models import Activity, ActivityMedia, Organization


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = [
            "slug",
            "email",
            "description",
            "website_url",
            "name",
            "goal",
            "year_founded",
            "status",
            "target_audience",
            "number_of_employees",
            "nuber_of_members",
            "number_of_volunteers",
            "location_lon",
            "location_lat",
            "address_city",
            "address_street",
            "address_house_num",
            "address_zipcode",
            "cities",
            "districts",
            "union_type",
        ]


class ActivityMediaSerializer(serializers.ModelSerializer):
    media_type = serializers.SerializerMethodField()

    class Meta:
        model = ActivityMedia
        fields = [
            "slug",
            "name",
            "media_type",
            "video_url",
            "image_url",
            "activity",
        ]

    def get_media_type(self, obj):
        if obj.video_url:
            return "video"
        elif obj.image_url:
            return "image"

    def validate(self, data):
        if data["video_url"] and data["image_url"]:
            raise serializers.ValidationError("Connot contain both image and video_url")
        return data

    def update(self, instance, validated_data):
        if validated_data["video_url"] and validated_data["image_url"]:
            raise serializers.ValidationError("Connot contain both image and video_url")
        return super().update(instance, validated_data)


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = [
            "slug",
            "name",
            "target_audience",
            "domain",
            "originization",
            "description",
            "contact_name",
            "phone_number",
            "logo",
            "phone_number",
        ]
