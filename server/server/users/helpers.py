from django.conf import settings
from django.contrib.auth.forms import PasswordResetForm


def send_user_invite(email):
    # send invitation to reset password & join the platform
    form_options = {
        "use_https": True,
        "from_email": getattr(settings, "DEFAULT_FROM_EMAIL"),
        # "request": request,
        "subject_template_name": "registration/password_reset_subject.txt",
        "email_template_name": "users/invite_with_password_reset.html",
        "extra_email_context": {"reset_base_url": settings.RESET_BASE_URL},
    }
    form = PasswordResetForm(data={"email": email})
    if form.is_valid():
        form.save(**form_options)
