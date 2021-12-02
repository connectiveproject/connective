from datetime import timedelta

import analytics
from django.db.models.signals import post_save
from django.dispatch import receiver

from server.utils.analytics_utils import event as analytics_event
from server.utils.analytics_utils import field as analytics_field

from .models import Event, EventOrder


def _track_events_creation(events):
    """
    track events creation using analytics
    :param events: list of Event objects to track
    """
    for e in events:
        analytics.track(
            analytics_field.UNKNOWN_SLUG,
            analytics_event.EVENT_CREATED,
            {
                "source": analytics_field.EVENT_CREATION_SOURCE_ACTIVITY_ORDER_APPROVAL,
                "slug": e.slug,
                "event_order_slug": e.event_order.slug,
                "start_time": e.start_time,
                "end_time": e.end_time,
                "school_group_slug": e.school_group.slug,
                "locations_name": e.locations_name,
                "is_canceled": e.is_canceled,
            },
        )


@receiver(post_save, sender=EventOrder)
def create_events_on_order_approval(sender, instance, created, **kwargs):
    if instance.status == EventOrder.Status.APPROVED and instance.events.count() == 0:
        if instance.recurrence == EventOrder.Recurrence.ONE_TIME:
            e = Event.objects.create(
                school_group=instance.school_group,
                locations_name=instance.locations_name,
                start_time=instance.start_time,
                end_time=instance.end_time,
                event_order=instance,
            )
            _track_events_creation([e])
            return

        events_to_create = []
        for i in range(0, 52):
            start_time = instance.start_time + timedelta(days=i * 7)
            end_time = instance.end_time + timedelta(days=i * 7)
            events_to_create.append(
                Event(
                    school_group=instance.school_group,
                    locations_name=instance.locations_name,
                    start_time=start_time,
                    end_time=end_time,
                    event_order=instance,
                )
            )
        Event.objects.bulk_create(events_to_create)
        _track_events_creation(events_to_create)


@receiver(post_save, sender=EventOrder)
def delete_events_on_order_cancellation(sender, instance, created, **kwargs):
    if instance.status == EventOrder.Status.CANCELLED:
        Event.objects.filter(event_order=instance).delete()
