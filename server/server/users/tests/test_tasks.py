import pytest
from celery.result import EagerResult

from server.users.tasks import get_users_count, send_user_invite_task
from server.users.tests.factories import ConsumerFactory, UserFactory

pytestmark = pytest.mark.django_db


def test_user_count(settings):
    """A basic test to execute the get_users_count Celery task."""
    UserFactory.create_batch(3)
    task_result = get_users_count.delay()
    assert isinstance(task_result, EagerResult)
    assert task_result.result == 3


def test_send_user_invite(settings):
    consumer = ConsumerFactory.create()
    # test with delay (celery, but without real celery process since CELERY_TASK_ALWAYS_EAGER = True)
    send_user_invite_task.delay(consumer.id, "Consumer")
    consumer.refresh_from_db()
    assert consumer.profile.invitation_count == 1
    # test without delay (synchronous call)
    send_user_invite_task(consumer.id, "Consumer")
    consumer.refresh_from_db()
    assert consumer.profile.invitation_count == 2
