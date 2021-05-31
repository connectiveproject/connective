from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import (
    Consumer,
    ConsumerProfile,
    Coordinator,
    CoordinatorProfile,
    User,
    Vendor,
    VendorProfile,
)


@receiver(post_save, sender=User)
@receiver(post_save, sender=Consumer)
@receiver(post_save, sender=Coordinator)
@receiver(post_save, sender=Vendor)
def update_user_profile(sender, instance, created, **kwargs):
    user_type_to_profile = {
        "COORDINATOR": CoordinatorProfile,
        "CONSUMER": ConsumerProfile,
        "VENDOR": VendorProfile,
    }

    if created and not hasattr(instance, "_no_profile_create"):
        user_type_to_profile[instance.user_type].objects.create(
            user=instance,
        )
