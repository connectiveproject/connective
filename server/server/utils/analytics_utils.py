import analytics


class Analytics:
    EVENT_SESSION_LOGIN = "session_login"
    EVENT_APP_LOGIN = "app_login"
    EVENT_INITIAL_PASSWORD_CREATED = "initial_password_created"

    @classmethod
    def identify_track(cls, user, event_name, properties=None):
        analytics.identify(
            user.slug,
            {
                "name": user.name,
                "email": user.email,
                "user_type": user.user_type,
            },
        )
        analytics.track(user.slug, event_name, properties)
