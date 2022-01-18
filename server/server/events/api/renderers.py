from server.utils.renderers import GenericCSVRenderer


class EventCSVRenderer(GenericCSVRenderer):
    fields = [
        "school_group_name",
        "school_name",
        "activity_name",
        "has_summary",
        "attended_consumers_count",
        "total_consumers_count",
        "instructor_name",
        "start_time",
        "end_time",
    ]
