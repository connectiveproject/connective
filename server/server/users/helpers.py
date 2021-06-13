from allauth.account.adapter import get_adapter
from allauth.account.forms import (
    EmailAwarePasswordResetTokenGenerator,
    ResetPasswordForm,
)
from allauth.account.utils import user_pk_to_url_str
from allauth.utils import build_absolute_uri
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse

default_token_generator = EmailAwarePasswordResetTokenGenerator()


class SendInviteForm(ResetPasswordForm):
    def save(self, request, **kwargs):
        current_site = get_current_site(request)
        email = self.cleaned_data["email"]
        token_generator = kwargs.get("token_generator", default_token_generator)

        for user in self.users:

            temp_key = token_generator.make_token(user)

            # save it to the password reset model
            # password_reset = PasswordReset(user=user, temp_key=temp_key)
            # password_reset.save()

            # send the password reset email
            path = reverse(
                "account_reset_password_from_key",
                kwargs=dict(uidb36=user_pk_to_url_str(user), key=temp_key),
            )
            url = build_absolute_uri(request, path)

            context = {
                "current_site": current_site,
                "user": user,
                "password_reset_url": url,
                "request": request,
            }

            # if app_settings.AUTHENTICATION_METHOD != AuthenticationMethod.EMAIL:
            #     context["username"] = user_username(user)
            get_adapter(request).send_mail(
                "account/email/password_reset_key", email, context
            )
        return self.cleaned_data["email"]


# def send_user_invite(email):
#     # send invitation to reset password & join the platform
#     form_options = {
#         "use_https": True,
#         "from_email": getattr(settings, "DEFAULT_FROM_EMAIL"),
#         # "request": request,
#         "subject_template_name": "registration/password_reset_subject.txt",
#         "email_template_name": "users/invite_with_password_reset.html",
#         "extra_email_context": {"reset_base_url": settings.RESET_BASE_URL},
#     }
#     form = PasswordResetForm(data={"email": email})
#     if form.is_valid():
#         form.save(**form_options)


def send_user_invite(email, request):
    # send invitation to reset password & join the platform
    form = SendInviteForm(data={"email": email})
    if form.is_valid():
        form.save(request)
