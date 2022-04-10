from rest_framework import serializers

from server.events.models import ConsumerEventFeedback, Event, EventOrder
from server.organizations.models import SchoolActivityGroup
from server.users.models import Consumer, Instructor
from server.utils.analytics_utils import event
from server.utils.analytics_utils.mixins import (
    TrackSerializerCreateMixin,
    TrackSerializerFieldUpdateMixin,
)


class EventOrderSerializer(
    TrackSerializerCreateMixin,
    TrackSerializerFieldUpdateMixin,
    serializers.ModelSerializer,
):
    tracker_on_create_event_name = event.EVENT_ORDER_CREATED
    tracker_on_field_update_event_name = event.EVENT_ORDER_STATUS_UPDATED
    tracker_props_fields = [
        "slug",
        "status",
        "recurrence",
        "school_group__slug",
        "locations_name",
        "start_time",
        "end_time",
        "school_group__activity_order__slug",
        "status_reason",
    ]
    tracker_fields_rename = {
        "school_group__slug": "school_group_slug",
        "school_group__activity_order__slug": "activity_order_slug",
    }
    tracker_fields_to_track = ["status"]

    school_group = serializers.SlugRelatedField(
        slug_field="slug",
        queryset=SchoolActivityGroup.objects.all(),
        required=False,
    )
    school_group_name = serializers.CharField(
        source="school_group.name",
        read_only=True,
    )
    activity_name = serializers.CharField(
        source="school_group.activity_order.activity.name",
        read_only=True,
    )
    school_name = serializers.CharField(
        source="school_group.activity_order.school.name",
        read_only=True,
    )
    additional_instructors = serializers.SlugRelatedField(
        many=True,
        read_only=False,
        queryset=Instructor.objects.all(),
        slug_field="slug",
        required=False,
    )
    instructor = serializers.SlugRelatedField(
        many=False,
        read_only=False,
        queryset=Instructor.objects.all(),
        slug_field="slug",
        required=False,
    )

    class Meta:
        model = EventOrder
        fields = [
            "slug",
            "status",
            "status_reason",
            "recurrence",
            "school_group",
            "locations_name",
            "start_time",
            "end_time",
            "created",
            "updated",
            "school_group_name",
            "activity_name",
            "school_name",
            "additional_instructors",
            "title",
            "instructor",
            "filter_grades",
            "filter_genders",
        ]
        read_only_fields = ["slug", "created", "updated"]

    def is_set(self, data, attribute):
        return attribute in data and data[attribute]

    def validate(self, data):
        """
        Check that start is before finish.
        """
        if (
            "end_time" in data
            and "start_time" in data
            and data["start_time"] > data["end_time"]
        ):
            raise serializers.ValidationError(
                {"end_time": "end time must occur after start time"}
            )
        if self.context["request"].method == "POST":
            data = self.validate_create(data)
        return data

    def validate_create(self, data):
        has_consumer_filters = self.is_set(data, "filter_grades") and self.is_set(
            data, "filter_genders"
        )
        if not has_consumer_filters and (
            self.is_set(data, "filter_genders") or self.is_set(data, "filter_grades")
        ):
            raise serializers.ValidationError(
                {
                    "filter_genders": "filter_genders and filter_grades must be set or empty together"
                }
            )
        if (has_consumer_filters and self.is_set(data, "school_group")) or (
            not has_consumer_filters and not self.is_set(data, "school_group")
        ):
            raise serializers.ValidationError(
                "one of school_group or filter_* fields must be set"
            )
        return data


class EventSerializerMixin(metaclass=serializers.SerializerMetaclass):
    activity_name = serializers.CharField(
        source="school_group.activity_order.activity.name",
        read_only=True,
    )
    activity_website = serializers.CharField(
        source="school_group.activity_order.activity.activity_website_url",
        read_only=True,
    )
    school_name = serializers.CharField(
        source="event_order.school.name",
        read_only=True,
    )
    school_group_name = serializers.SerializerMethodField(read_only=True)
    consumers = serializers.SlugRelatedField(
        slug_field="slug",
        queryset=Consumer.objects.all(),
        many=True,
        required=False,
    )
    school_group = serializers.SlugRelatedField(
        slug_field="slug",
        queryset=SchoolActivityGroup.objects.all(),
    )

    def get_school_group_name(self, obj):
        event: Event = obj
        return event.group_display_name()

    def validate(self, data):
        """
        Check that start is before finish.
        """
        if (
            "end_time" in data
            and "start_time" in data
            and data["start_time"] > data["end_time"]
        ):
            raise serializers.ValidationError(
                {"end_time": "end time must occur after start time"}
            )
        return data


class EventSerializer(
    TrackSerializerFieldUpdateMixin, EventSerializerMixin, serializers.ModelSerializer
):
    tracker_on_field_update_event_name = event.EVENT_SUMMARY_CREATED
    tracker_props_fields = [
        "slug",
        "event_order__slug",
        "event_order__school_group__slug",
        "start_time",
        "end_time",
        "consumers__COUNT",
        "locations_name",
        "has_summary",
        "summary_general_rating",
        "summary_children_behavior",
        "is_canceled",
        "cancellation_reason",
    ]

    tracker_fields_rename = {
        "event_order__slug": "event_order_slug",
        "event_order__school_group__slug": "school_group_slug",
        "consumers__COUNT": "consumers_count",
        "school_group__slug": "school_group_slug",
    }
    tracker_fields_to_track = ["has_summary"]

    total_consumers_count = serializers.SerializerMethodField(read_only=True)
    is_series_event = serializers.SerializerMethodField(read_only=True)
    attended_consumers_count = serializers.SerializerMethodField(read_only=True)
    instructor_name = serializers.CharField(
        source="instructor.name", default="", read_only=True
    )

    class Meta:
        model = Event
        fields = [
            "slug",
            "event_order",
            "activity_name",
            "activity_website",
            "school_group_name",
            "start_time",
            "end_time",
            "consumers",
            "school_name",
            "school_group",
            "locations_name",
            "has_summary",
            "summary_general_notes",
            "summary_general_rating",
            "summary_children_behavior",
            "is_canceled",
            "cancellation_reason",
            "ext_consumers_attended",
            "total_consumers_count",
            "attended_consumers_count",
            "instructor_name",
            "is_series_event",
            "title",
        ]
        read_only_fields = [
            "slug",
            "event_order",
            "total_consumers_count",
            "attended_consumers_count",
            "instructor_name",
        ]

    def get_total_consumers_count(self, obj):
        if (
            not obj.school_group
            or obj.school_group.group_type
            == SchoolActivityGroup.GroupTypes.NO_REGISTRATION
        ):
            return "-"
        return obj.school_group.consumers.count()

    def get_attended_consumers_count(self, obj):
        if (
            not obj.school_group
            or obj.school_group.group_type
            == SchoolActivityGroup.GroupTypes.NO_REGISTRATION
        ):
            return obj.ext_consumers_attended
        return obj.consumers.count()

    def get_is_series_event(self, obj):
        return bool(obj.series)


class ConsumerEventSerializer(EventSerializerMixin, serializers.ModelSerializer):
    has_feedback = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = [
            "slug",
            "activity_name",
            "school_group_name",
            "start_time",
            "end_time",
            "consumers",
            "school_group",
            "locations_name",
            "has_feedback",
        ]

    def get_has_feedback(self, obj):
        user = self.context["request"].user
        return ConsumerEventFeedback.objects.filter(
            event=obj.pk,
            consumer=user,
        ).exists()


class ConsumerEventFeedbackSerializer(serializers.ModelSerializer):
    event = serializers.SlugRelatedField(
        slug_field="slug",
        queryset=Event.objects.all(),
    )
    consumer = serializers.SlugRelatedField(
        slug_field="slug",
        read_only=True,
    )

    class Meta:
        model = ConsumerEventFeedback
        fields = [
            "slug",
            "event",
            "consumer",
            "general_notes",
            "secondary_notes",
            "general_rating",
            "secondary_rating",
        ]
        read_only_fields = ["slug"]
