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


def serializer_create_track(event_name, props_fields, fields_rename={}):
    """
    decorator used for event tracking (analytics) on serializer create() calls

    :string event_name: name of the event to be tracked
    :list props_fields: model fields to add as props to tracker
    :dict fields_rename: model fields rename. format: { original_field: new_field, ... }
    """

    def outer_wrapper(serializer_create):
        def wrapper(self, validated_data):
            result = serializer_create(self, validated_data)
            props = {
                fields_rename.get(k) or k: v
                for k, v in validated_data.items()
                if k in props_fields
            }
            analytics.track(self.context["request"].user.slug, event_name, props)
            return result

        return wrapper

    return outer_wrapper
