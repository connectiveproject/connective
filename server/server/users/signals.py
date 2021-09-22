from allauth.account.signals import user_logged_in
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from server.utils.analytics_utils import identify_track
from server.utils.analytics_utils.constants import EVENT_SESSION_LOGIN

from .models import (
    Consumer,
    ConsumerProfile,
    Coordinator,
    CoordinatorProfile,
    Instructor,
    InstructorProfile,
    Supervisor,
    SupervisorProfile,
    Vendor,
    VendorProfile,
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


@receiver(user_logged_in)
def post_login(sender, user, request, **kwargs):
    identify_track(user, EVENT_SESSION_LOGIN)
