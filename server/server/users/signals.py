from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import ConsumerProfile, CoordinatorProfile, User, VendorProfile


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    user_type_to_profile = {
        "COORDINATOR": CoordinatorProfile,
        "CONSUMER": ConsumerProfile,
        "VENDOR": VendorProfile,
    }

    if created:
        user_type_to_profile[instance.user_type].objects.create(
            user=instance,
        )
