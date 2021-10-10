from django.contrib.auth import get_user_model

from config import celery_app
from server.users.helpers import send_user_invite
from server.users.models import USER_TYPE_TO_MODEL

User = get_user_model()


@celery_app.task
def get_users_count():
    """A pointless Celery task to demonstrate usage."""
    print("starting....")
    return User.objects.count()


@celery_app.task
def send_user_invite_task(user_id, user_type):
    user = USER_TYPE_TO_MODEL.get(user_type).objects.get(id=user_id)
    send_user_invite(user)
