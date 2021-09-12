from server.users.forms import SendInviteForm


def send_user_invite(email):
    # send invitation to reset password & join the platform
    form = SendInviteForm(data={"email": email})
    if form.is_valid():
        form.save(None)
