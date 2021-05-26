import pytest

from server.users.models import User

pytestmark = pytest.mark.django_db


def test_user_get_absolute_url(user: User):
    assert user.get_absolute_url() == f"/users/{user.username}/"


def test_profile_auto_creation(user: User):
    assert hasattr(user, "consumerprofile")
    assert not hasattr(user, "vendorprofile")
    assert not hasattr(user, "coordinatorprofile")
