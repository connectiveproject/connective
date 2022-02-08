from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from taggit.serializers import TaggitSerializer, TagListSerializerField

from server.organizations.models import (
    Activity,
    ActivityMedia,
    Organization,
    SchoolActivityGroup,
    SchoolActivityOrder,
)
from server.schools.models import School
from server.users.models import Consumer, Instructor
from server.utils.analytics_utils import event
from server.utils.analytics_utils.mixins import (
    TrackSerializerCreateMixin,
    TrackSerializerFieldUpdateMixin,
)


class OrganizationSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(read_only=True)

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
            "number_of_members",
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
    activity = serializers.SlugRelatedField(
        queryset=Activity.objects.all(), slug_field="slug"
    )

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
        if data.get("video_url") and data.get("image_url"):
            raise serializers.ValidationError("Cannot contain both image and video_url")
        return data

    def update(self, instance, validated_data):
        if validated_data.get("video_url") and validated_data.get("image_url"):
            raise serializers.ValidationError("Cannot contain both image and video_url")
        return super().update(instance, validated_data)


class ActivitySerializer(TaggitSerializer, serializers.ModelSerializer):
    is_ordered = serializers.SerializerMethodField()
    order_status = serializers.SerializerMethodField()
    tags = TagListSerializerField()

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
            "is_ordered",
            "order_status",
            "tags",
        ]

    def get_order_status(self, obj):
        user = self.context["request"].user

        try:
            return SchoolActivityOrder.objects.get(
                school=user.school_member.school,
                activity=obj,
            ).status

        except ObjectDoesNotExist:
            return "NOT_ORDERED"

    def get_is_ordered(self, obj):
        user = self.context["request"].user
        if not hasattr(user, "school_member"):
            return False

        return (
            SchoolActivityOrder.objects.filter(
                school=user.school_member.school,
                activity=obj,
            )
            .exclude(status=SchoolActivityOrder.Status.CANCELLED)
            .exists()
        )


class VendorActivitySerializer(
    TaggitSerializer, TrackSerializerCreateMixin, serializers.ModelSerializer
):
    tracker_on_create_event_name = event.ACTIVITY_CREATED
    tracker_props_fields = ["slug", "name", "domain"]

    tags = TagListSerializerField()

    class Meta:
        model = Activity
        fields = [
            "slug",
            "name",
            "target_audience",
            "domain",
            "originization",
            "activity_website_url",
            "activity_email",
            "description",
            "contact_name",
            "logo",
            "phone_number",
            "tags",
        ]
        read_only_fields = ["slug", "originization"]


class ConsumerActivitySerializer(TaggitSerializer, serializers.ModelSerializer):
    JOINED = "JOINED"
    NOT_JOINED = "NOT_JOINED"
    PENDING_GROUP_ASSIGNMENT = "PENDING_GROUP_ASSIGNMENT"

    consumer_join_status = serializers.SerializerMethodField()
    is_consumer_joined = serializers.SerializerMethodField()
    tags = TagListSerializerField()

    class Meta:
        model = Activity
        fields = [
            "slug",
            "name",
            "target_audience",
            "originization",
            "description",
            "logo",
            "consumer_join_status",
            "is_consumer_joined",
            "tags",
        ]

    def get_consumer_join_status(self, obj):
        user = self.context["request"].user
        # check if consumer is in a group
        assigned_groups = SchoolActivityGroup.objects.filter(
            activity_order__activity=obj,
            consumers=user,
        ).exclude(group_type=SchoolActivityGroup.GroupTypes.DISABLED_CONSUMERS)

        if not assigned_groups.exists():
            return ConsumerActivitySerializer.NOT_JOINED

        elif (
            assigned_groups[0].group_type
            == SchoolActivityGroup.GroupTypes.CONTAINER_ONLY
        ):
            return ConsumerActivitySerializer.PENDING_GROUP_ASSIGNMENT

        return ConsumerActivitySerializer.JOINED

    def get_is_consumer_joined(self, obj):
        user = self.context["request"].user
        if not hasattr(user, "school_member"):
            return False

        if (
            SchoolActivityGroup.objects.filter(
                activity_order__activity=obj,
                consumers=user,
            )
            .exclude(group_type=SchoolActivityGroup.GroupTypes.DISABLED_CONSUMERS)
            .exists()
        ):
            return True
        return False


class ManageSchoolActivitySerializer(
    TrackSerializerFieldUpdateMixin, serializers.ModelSerializer
):
    tracker_on_field_update_event_name = event.ACTIVITY_ORDER_STATUS_UPDATED
    tracker_props_fields = ["slug", "activity__slug", "school__slug", "status"]
    tracker_fields_to_track = ["status"]
    tracker_fields_rename = {
        "activity__slug": "activity_slug",
        "school__slug": "school_slug",
    }

    school = serializers.SlugRelatedField(
        queryset=School.objects.all(), slug_field="slug"
    )
    activity = serializers.SlugRelatedField(
        queryset=Activity.objects.all(), slug_field="slug"
    )
    requested_by = serializers.CharField(source="requested_by.slug", read_only=True)
    last_updated_by = serializers.CharField(
        source="last_updated_by.slug",
        read_only=True,
    )
    activity_name = serializers.CharField(source="activity.name", read_only=True)

    class Meta:
        model = SchoolActivityOrder
        read_only_fields = (
            "slug",
            "created_at",
            "updated_at",
        )
        fields = [
            "slug",
            "requested_by",
            "last_updated_by",
            "school",
            "activity",
            "status",
            "created_at",
            "updated_at",
            "activity_name",
        ]

    def validate(self, data):
        """
        Check if the school is under the user & validate status
        """
        user = self.context["request"].user
        if (
            not hasattr(user, "school_member")
            or not data["school"] == user.school_member.school
        ):
            raise serializers.ValidationError({"school": "must be a school member"})

        if "status" in data and data["status"] not in [
            SchoolActivityOrder.Status.CANCELLED,
            SchoolActivityOrder.Status.PENDING_ADMIN_APPROVAL,
        ]:
            raise serializers.ValidationError({"status": "invalid status"})

        return data


class SchoolActivityGroupSerializer(
    TrackSerializerCreateMixin, serializers.ModelSerializer
):
    tracker_on_create_event_name = event.ACTIVITY_GROUP_CREATED
    tracker_props_fields = ["slug", "name", "group_type", "activity_order__slug"]
    tracker_fields_rename = {"activity_order__slug": "activity_order_slug"}

    instructor_name = serializers.CharField(
        source="instructor.name",
        read_only=True,
    )
    instructor = serializers.SlugRelatedField(
        queryset=Instructor.objects.all(),
        slug_field="slug",
        required=False,
    )
    activity_logo = serializers.ImageField(
        source="activity_order.activity.logo",
        read_only=True,
    )
    activity_name = serializers.CharField(
        source="activity_order.activity.name",
        read_only=True,
    )
    activity_order = serializers.SlugRelatedField(
        queryset=SchoolActivityOrder.objects.all(), slug_field="slug"
    )
    school_name = serializers.CharField(
        source="activity_order.school.name",
        read_only=True,
    )
    school_slug = serializers.CharField(
        source="activity_order.school.slug",
        read_only=True,
    )
    consumers = serializers.SlugRelatedField(
        queryset=Consumer.objects.all(),
        slug_field="slug",
        many=True,
        required=False,
    )

    class Meta:
        model = SchoolActivityGroup
        fields = [
            "slug",
            "activity_logo",
            "activity_name",
            "activity_order",
            "name",
            "description",
            "consumers",
            "group_type",
            "instructor",
            "instructor_name",
            "school_name",
            "school_slug",
        ]


class ConsumerRequestDataSerializer(serializers.ModelSerializer):

    activity_name = serializers.CharField(
        source="activity_order.activity.name",
        read_only=True,
    )
    activity_order = serializers.CharField(
        source="activity_order.slug",
        read_only=True,
    )
    consumer_requests = serializers.IntegerField()

    class Meta:
        model = SchoolActivityGroup
        fields = [
            "activity_name",
            "activity_order",
            "consumer_requests",
        ]
