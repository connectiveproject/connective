from django.contrib.auth import get_user_model

from config import celery_app
from server.users.helpers import send_user_invite

User = get_user_model()


@celery_app.task
def get_users_count():
    """A pointless Celery task to demonstrate usage."""
    print("starting....")
    return User.objects.count()


# command to run celery worker:
# celery -A config.celery_app worker
#
# conf for activate async calls:
# settings.CELERY_TASK_ALWAYS_EAGER=False
#
# code for submit async call for this function:
# send_mail.delay('1','2','3')
#
@celery_app.task
def send_mail_sync(subject, to, content):
    print(f"Subject: {subject}, To: {to}, Content: {content}")


@celery_app.task
def send_user_invite_task(email):
    print("in send_user_invite_task")
    send_user_invite(email)
