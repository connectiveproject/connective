from django.dispatch import Signal, receiver

activity_order_created_signal: Signal = Signal()


@receiver(activity_order_created_signal)
def activity_order_created(sender, **kwargs):  # noqa:F811
    pass  # do nothing for now
