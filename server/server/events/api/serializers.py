from rest_framework import serializers

from server.events.models import Event


class BaseEventSerializer(serializers.ModelSerializer):
    activity_name = serializers.CharField(
        source="school_group.activity_order.activity.name",
        read_only=True,
    )
    school_group_name = serializers.CharField(
        source="school_group.name",
        read_only=True,
    )

    def validate(self, data):
        """
        Check that start is before finish.
        """
        if data["start_time"] > data["end_time"]:
            raise serializers.ValidationError(
                {"end_time": "end time must occur after start time"}
            )
        return data


class EventSerializer(BaseEventSerializer):
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
            "has_summary",
            "summary_general_notes",
            "summary_general_rating",
            "summary_children_behavior",
        ]


class ConsumerEventSerializer(BaseEventSerializer):
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
        ]
