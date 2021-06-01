import pytest

from server.schools.models import School
from server.schools.tests.factories import SchoolFactory
from server.users.models import Consumer, Coordinator, User
from server.users.tests.factories import (
    ConsumerFactory,
    CoordinatorFactory,
    UserFactory,
)


@pytest.fixture(autouse=True)
def media_storage(settings, tmpdir):
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture
def user() -> User:
    return UserFactory()


@pytest.fixture
def coordinator() -> Coordinator:
    return CoordinatorFactory()


@pytest.fixture
def consumer() -> Consumer:
    return ConsumerFactory()


@pytest.fixture
def school() -> School:
    return SchoolFactory()
