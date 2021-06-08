import pytest

from server.users.models import (
    Consumer,
    ConsumerProfile,
    Coordinator,
    CoordinatorProfile,
    Vendor,
    VendorProfile,
)

pytestmark = pytest.mark.django_db


def test_update_user_profile_signal():
    consumer = Consumer.objects.create(email="consy_the_consumer@example.com")
    coordinator = Coordinator.objects.create(email="cordy_the_coordinator@example.com")
    vendor = Vendor.objects.create(email="vendy_the_vendor@example.com")

    assert isinstance(consumer.profile, ConsumerProfile)
    assert isinstance(coordinator.profile, CoordinatorProfile)
    assert isinstance(vendor.profile, VendorProfile)
