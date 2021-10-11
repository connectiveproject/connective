from celery.utils.log import get_task_logger
from django.contrib.auth import get_user_model

from config import celery_app
from server.users.helpers import send_user_invite
from server.users.models import USER_TYPE_TO_MODEL
from server.utils.logging.constants import INVITE_USER

User = get_user_model()

logger = get_task_logger(__name__)


@celery_app.task
def get_users_count():
    """A pointless Celery task to demonstrate usage."""
    return User.objects.count()


@celery_app.task
def send_user_invite_task(user_id, user_type):
    logger.info(f"{INVITE_USER} : { user_type} : {user_id}")
    user = USER_TYPE_TO_MODEL.get(user_type).objects.get(id=user_id)
    send_user_invite(user)
