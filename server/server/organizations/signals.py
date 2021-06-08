from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import SchoolActivityGroup, SchoolActivityOrder


@receiver(post_save, sender=SchoolActivityOrder)
def update_user_profile(sender, instance, **kwargs):
    """
    on order approval, create a default school-activity-group
    """
    if instance.status == SchoolActivityOrder.Status.APPROVED:
        if not len(SchoolActivityGroup.objects.filter(activity_order=instance)):
            SchoolActivityGroup.objects.create(
                activity_order=instance,
                name="Default Group",
                description="Default Group",
                container_only=True,
            )
