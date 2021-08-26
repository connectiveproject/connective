from rest_framework import serializers

from server.events.models import ConsumerEventFeedback, Event, EventOrder
from server.organizations.models import SchoolActivityGroup

from django.apps import apps

Consumer = apps.get_model("users.Consumer")

class EventOrderSerializer(serializers.ModelSerializer):
    school_group = serializers.SlugRelatedField(
        slug_field="slug",
        queryset=SchoolActivityGroup.objects.all(),
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
        ]
        read_only_fields = ["slug", "created", "updated"]

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


class EventSerializerMixin(metaclass=serializers.SerializerMetaclass):
    activity_name = serializers.CharField(
        source="school_group.activity_order.activity.name",
        read_only=True,
    )
    activity_website = serializers.CharField(
        source="school_group.activity_order.activity.activity_website_url",
        read_only=True,
    )
    school_group_name = serializers.CharField(
        source="school_group.name",
        read_only=True,
    )
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


class EventSerializer(EventSerializerMixin, serializers.ModelSerializer):
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
            "school_group",
            "locations_name",
            "has_summary",
            "summary_general_notes",
            "summary_general_rating",
            "summary_children_behavior",
        ]
        read_only_fields = ["slug", "event_order"]


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
