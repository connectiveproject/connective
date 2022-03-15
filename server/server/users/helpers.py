import logging
from typing import Dict

import requests
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

from server.users.models import Notification, User
from server.users.notifications import NotificationRegistry
from server.utils.factories import ConnectiveUtils, get_form_factory, get_utils
from server.utils.logging.constants import CAPTCHA, PROFILE

logger = logging.getLogger(__name__)
utils: ConnectiveUtils = get_utils()
CUSTOMER_EMAIL_ENABLED = utils.customer_email_enabled


def send_user_invite(user):
    if not CUSTOMER_EMAIL_ENABLED:
        logger.info(f"Customer email is disabled. User: {user}")
        return
    form_factory = get_form_factory()
    form = form_factory.create_send_invite_form(user)
    if form.is_valid():
        form.save(None)
        try:
            profile = user.profile
            profile.invitation_count = profile.invitation_count + 1
            profile.last_invite_sent = timezone.now()
            profile.save()
        except ObjectDoesNotExist:
            logger.exception(
                f"{PROFILE}: cannot fetch profile for user {user}. pk={user.pk}"
            )


def send_password_recovery(email):
    # send password recovery email
    form_factory = get_form_factory()
    form = form_factory.create_recover_password_form(email)
    if form.is_valid():
        form.save(None)


def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        return x_forwarded_for.split(",")[0]
    return request.META.get("REMOTE_ADDR")


def is_recaptcha_token_valid(token, request=None):
    try:
        if not token:
            return False

        data = {
            "secret": settings.GOOGLE_RECAPTCHA_SECRET_KEY,
            "response": token,
        }
        if request:
            data["remoteip"] = get_client_ip(request)

        response = requests.post(settings.RECAPTCHA_VALIDATION_URL, data)
        return response.json()["success"]

    except Exception:
        logger.exception(CAPTCHA)
        return False


def trigger_notification(
    registry: NotificationRegistry, user: User, parameters: Dict[str, str]
) -> Notification:
    # We don't want to show identical notifications again and again.
    # check for existing identical new notification:
    existing_notification: Notification = (
        Notification.objects.filter(user=user)
        .filter(status="NEW")
        .filter(notification_code=registry.code)
        .filter(parameters=parameters)
        .first()
    )
    if existing_notification:
        # we have identical notification - just update its date
        existing_notification.created_at = timezone.now()
        existing_notification.save()
        return existing_notification
    else:
        notification: Notification = Notification.objects.create(
            notification_code=registry.code, user=user, parameters=parameters
        )
    return notification
