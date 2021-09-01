from server.users.forms import RecoverPasswordForm, SendInviteForm


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
