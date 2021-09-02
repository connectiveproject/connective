import logging

import requests
from django.conf import settings

from server.users.forms import RecoverPasswordForm, SendInviteForm
from server.utils.logging.constants import CAPTCHA

logger = logging.getLogger(__name__)


def send_user_invite(email):
    # send invitation to reset password & join the platform
    form = SendInviteForm(data={"email": email})
    if form.is_valid():
        form.save(None)


def send_password_recovery(email):
    # send password recovery email
    form = RecoverPasswordForm(data={"email": email})
    if form.is_valid():
        form.save(None)


def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        return x_forwarded_for.split(",")[0]
    return request.META.get("REMOTE_ADDR")


def is_recaptcha_token_valid(token, request=None):
    try:
        if not settings.SHOULD_VALIDATE_RECAPTCHA:
            return True

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
