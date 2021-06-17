from rest_framework import serializers

from server.events.models import Event


class EventSerializer(serializers.ModelSerializer):
    activity_name = serializers.CharField(
        source="school_group.activity_order.activity.name",
        read_only=True,
    )
    school_group_name = serializers.CharField(
        source="school_group.name",
        read_only=True,
    )

    class Meta:
        model = Event
        fields = [
            "activity_name",
            "school_group_name",
            "start_time",
            "end_time",
            "consumers",
            "school_group",
            "locations_name",
        ]

    def validate(self, data):
        """
        Check that start is before finish.
        """
        if data["start_time"] > data["end_time"]:
            raise serializers.ValidationError(
                {"end_time": "end time must occur after start time"}
            )
        return data
