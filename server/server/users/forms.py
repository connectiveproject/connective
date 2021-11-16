from os import path

from allauth.account.forms import (
    EmailAwarePasswordResetTokenGenerator,
    ResetPasswordForm,
)
from allauth.account.utils import user_pk_to_url_str
from django.conf import settings
from django.contrib.auth import forms as admin_forms
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class UserChangeForm(admin_forms.UserChangeForm):
    class Meta(admin_forms.UserChangeForm.Meta):
        model = User


class UserCreationForm(admin_forms.UserCreationForm):
    class Meta(admin_forms.UserCreationForm.Meta):
        model = User

        error_messages = {
            "username": {"unique": _("This username has already been taken.")}
        }


class ResetPasswordGenericMixin:
    """
    used to send an invitation to onboard the platform and reset the password
    """

    default_token_generator = EmailAwarePasswordResetTokenGenerator()
    # override these for customization
    email_text_filepath = ""
    email_html_filepath = ""
    email_title = ""
    client_uri = ""

    def send_email_invite(self, email, uri, uid, token):
        context = {
            "uri": uri,
            "uid": uid,
            "token": token,
        }
        msg_plain = render_to_string(self.email_text_filepath, context)
        msg_html = render_to_string(self.email_html_filepath, context)
        send_mail(
            self.email_title,
            msg_plain,
            None,
            [email],
            html_message=msg_html,
        )

    def save(self, request, **kwargs):
        email = self.cleaned_data["email"]
        token_generator = kwargs.get("token_generator", self.default_token_generator)
        for user in self.users:
            temp_key = token_generator.make_token(user)
            self.send_email_invite(
                email,
                self.client_uri,
                user_pk_to_url_str(user),
                temp_key,
            )
        return self.cleaned_data["email"]


class SendInviteForm(ResetPasswordGenericMixin, ResetPasswordForm):
    email_text_filepath = "users/invite_with_password_reset.txt"
    email_html_filepath = "users/invite_with_password_reset.html"
    email_title = "Welcome To Connective!"
    client_uri = path.join(settings.CLIENT_BASE_URL, "he/welcome/reset-password/init")


class RecoverPasswordForm(ResetPasswordGenericMixin, ResetPasswordForm):
    email_text_filepath = "users/recover_password.txt"
    email_html_filepath = "users/recover_password.html"
    email_title = "Connective Password Reset"
    client_uri = path.join(
        settings.CLIENT_BASE_URL, "he/welcome/reset-password/recover"
    )


class ConnectiveFormFactory:
    def create_send_invite_form(user: User) -> SendInviteForm:
        email = user.email
        return SendInviteForm(data={"email": email})

    def create_recover_password_form(email: str) -> RecoverPasswordForm:
        return RecoverPasswordForm(data={"email": email})
