from allauth.account.forms import (
    EmailAwarePasswordResetTokenGenerator,
    ResetPasswordForm,
)
from django.conf import settings
from allauth.account.utils import user_pk_to_url_str
from django.core.mail import send_mail
from django.template.loader import render_to_string

from os import path


class SendInviteForm(ResetPasswordForm):
    default_token_generator = EmailAwarePasswordResetTokenGenerator()

    def send_email_invite(self, email, uri, uid, token):
      # add header
      # make url work
      # change msg_plain
      # add css
      msg_plain = "render_to_string('templates/email.txt', {'some_params': some_params})"
      msg_html = render_to_string('users/invite_with_password_reset.html', {"uri": uri, "uid": uid, "token": token})
      send_mail(
          'email title',
          msg_plain,
          'some@sender.com',
          [email],
          html_message=msg_html,
      )

    def save(self, request, **kwargs):
        email = self.cleaned_data["email"]
        token_generator = kwargs.get("token_generator", self.default_token_generator)
        for user in self.users:
            temp_key = token_generator.make_token(user)
            import logging
            logger = logging.getLogger("root")
            logger.warn("settings.CLIENT_BASE_URL")
            logger.warn(settings.CLIENT_BASE_URL)

            uri = path.join(settings.CLIENT_BASE_URL, "he/welcome/reset-password")
            logger.warn(uri)
            self.send_email_invite(email, uri, user_pk_to_url_str(user), temp_key)
        return self.cleaned_data["email"]


def send_user_invite(email, request):
    # send invitation to reset password & join the platform
    form = SendInviteForm(data={"email": email})
    if form.is_valid():
        form.save(request)
