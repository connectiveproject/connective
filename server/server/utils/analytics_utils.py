import analytics

EVENT_SESSION_LOGIN = "session_login"
EVENT_APP_LOGIN = "app_login"
EVENT_INITIAL_PASSWORD_CREATED = "initial_password_created"
EVENT_ACTIVITY_CREATED = "activity_created"


def identify_track(user, event_name, properties=None):
    analytics.identify(
        user.slug,
        {
            "name": user.name,
            "email": user.email,
            "user_type": user.user_type,
        },
    )
    return analytics.track(user.slug, event_name, properties)


def serializer_create_track(event_name, prop_fields, fields_rename={}):
    """
    :list prop_fields: model fields to add as props
    """

    def track_deco(func):
        """
        decorator used for tracking serializer create() func calls
        """

        def wrapper(self, validated_data):
            import ipdb

            ipdb.set_trace()
            result = func(validated_data)
            props = {
                fields_rename.get(k) or k: v
                for k, v in validated_data.items()
                if k in prop_fields
            }
            analytics.track(self.context["request"].user.slug, event_name, props)
            return result

        return wrapper

    return track_deco
