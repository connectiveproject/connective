from datetime import timedelta

from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Event, EventOrder


@receiver(post_save, sender=EventOrder)
def create_events_on_order_approval(sender, instance, created, **kwargs):
    if instance.status == EventOrder.Status.APPROVED and instance.events.count() == 0:
        if instance.recurrence == EventOrder.Recurrence.ONE_TIME:
            return Event.objects.create(
                school_group=instance.school_group,
                locations_name=instance.locations_name,
                start_time=instance.start_time,
                end_time=instance.end_time,
                event_order=instance,
            )

        events_to_create = []
        for i in range(0, 54):
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


@receiver(post_save, sender=EventOrder)
def delete_events_on_order_cancellation(sender, instance, created, **kwargs):
    if instance.status == EventOrder.Status.CANCELLED:
        Event.objects.filter(event_order=instance).delete()
