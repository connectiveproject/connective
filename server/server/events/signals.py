import zoneinfo
from datetime import timedelta

import analytics
from django.db.models.signals import post_save
from django.dispatch import receiver

from server.utils.analytics_utils import event as analytics_event
from server.utils.analytics_utils import field as analytics_field
from server.utils.factories import ConnectiveUtils, get_utils

from .models import Event, EventOrder, EventSeries


def _track_events_creation(events):
    """
    track events creation using analytics
    :param events: list of Event objects to track
    """
    for e in events:
        school_group_slug = "NO_GROUP"
        if e.school_group:
            school_group_slug = e.school_group.slug
        analytics.track(
            analytics_field.UNKNOWN_SLUG,
            analytics_event.EVENT_CREATED,
            {
                "source": analytics_field.EVENT_CREATION_SOURCE_ACTIVITY_ORDER_APPROVAL,
                "slug": e.slug,
                "event_order_slug": e.event_order.slug,
                "start_time": e.start_time,
                "end_time": e.end_time,
                "school_group_slug": school_group_slug,
                "locations_name": e.locations_name,
                "is_canceled": e.is_canceled,
            },
        )


@receiver(post_save, sender=EventOrder)
def create_events_on_order_approval(sender, instance, created, **kwargs):
    if instance.status == EventOrder.Status.APPROVED and instance.events.count() == 0:
        instructor = instance.instructor
        if not instructor:
            instructor = instance.school_group.instructor
        if instance.recurrence == EventOrder.Recurrence.ONE_TIME:
            e = Event.objects.create(
                school_group=instance.school_group,
                locations_name=instance.locations_name,
                start_time=instance.start_time,
                end_time=instance.end_time,
                instructor=instructor,
                title=instance.title,
                filter_genders=instance.filter_genders,
                filter_grades=instance.filter_grades,
                event_order=instance,
            )
            e.additional_instructors.set(instance.additional_instructors.all())
            _track_events_creation([e])
            return

        event_series = EventSeries.objects.create()

        events_to_create = []
        utils: ConnectiveUtils = get_utils()
        # create reoccuring events. Since server time is in UTC, we need to take into account the timezone of the
        # customer, otherwise we will create future events with wrong UTC offset when DST changes. So the idea is
        # to iterate over events in customer timezone, and save them in UTC.
        timezone_str: str = utils.get_customer_time_zone()
        customer_timezone = zoneinfo.ZoneInfo(timezone_str)
        utc_timezone = zoneinfo.ZoneInfo("UTC")
        first_start_customer_tz = instance.start_time.astimezone(customer_timezone)
        first_end_customer_tz = instance.end_time.astimezone(customer_timezone)
        for i in range(0, 52):
            # start/end time in customer timezone:
            start_time_customer_tz = first_start_customer_tz + timedelta(days=i * 7)
            end_time_customer_tz = first_end_customer_tz + timedelta(days=i * 7)
            events_to_create.append(
                Event(
                    series=event_series,
                    school_group=instance.school_group,
                    locations_name=instance.locations_name,
                    # start/end time in UTC:
                    start_time=start_time_customer_tz.astimezone(utc_timezone),
                    end_time=end_time_customer_tz.astimezone(utc_timezone),
                    instructor=instructor,
                    title=instance.title,
                    filter_genders=instance.filter_genders,
                    filter_grades=instance.filter_grades,
                    event_order=instance,
                )
            )
        Event.objects.bulk_create(events_to_create)

        for event in events_to_create:
            event.additional_instructors.set(instance.additional_instructors.all())
        _track_events_creation(events_to_create)


@receiver(post_save, sender=EventOrder)
def delete_events_on_order_cancellation(sender, instance, created, **kwargs):
    if instance.status == EventOrder.Status.CANCELLED:
        Event.objects.filter(event_order=instance).delete()
