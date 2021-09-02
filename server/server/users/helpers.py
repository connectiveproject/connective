import requests

from server.users.forms import RecoverPasswordForm, SendInviteForm

RECAPTCHA_VALIDATION_URL = "https://www.google.com/recaptcha/api/siteverify"


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


secret_key = ""  # Preferably from settings.py // console.log(move)


def is_recaptcha_token_valid(token, request=None):
    """
    TODO: move to celery
    """
    if not token:
        return False

    data = {
        "secret": secret_key,
        "response": token,
    }
    if request:
        data["remoteip"] = get_client_ip(request)

    response = requests.post(RECAPTCHA_VALIDATION_URL, data)
    return response.json()["success"]
