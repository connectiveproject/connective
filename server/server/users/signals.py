from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import (
    ConsumerProfile,
    CoordinatorProfile,
    InstructorProfile,
    SupervisorProfile,
    VendorProfile,
    Consumer,
    Coordinator,
    Instructor,
    Vendor,
    Supervisor,
)

@receiver(post_save, sender=Consumer)
@receiver(post_save, sender=Coordinator)
@receiver(post_save, sender=Instructor)
@receiver(post_save, sender=Vendor)
@receiver(post_save, sender=Supervisor)
def update_user_profile(sender, instance, created, **kwargs):
    user_type_to_profile = {
        get_user_model().Types.COORDINATOR: CoordinatorProfile,
        get_user_model().Types.CONSUMER: ConsumerProfile,
        get_user_model().Types.INSTRUCTOR: InstructorProfile,
        get_user_model().Types.VENDOR: VendorProfile,
        get_user_model().Types.SUPERVISOR: SupervisorProfile,
    }

    if created:
        user_type_to_profile[instance.user_type].objects.create(
            user=instance,
        )
