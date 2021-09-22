import analytics

from .helpers import get_nested_obj_attr_value

EVENT_SESSION_LOGIN = "session_login"
EVENT_APP_LOGIN = "app_login"
EVENT_INITIAL_PASSWORD_CREATED = "initial_password_created"
EVENT_ACTIVITY_CREATED = "activity_created"
EVENT_ACTIVITY_ORDER_STATUS_UPDATED = "activity_order_status_updated"


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


def track_serializer_create(event_name, props_fields, fields_rename={}):
    """
    decorator used for event tracking (analytics) on serializer create() calls

    :string event_name: name of the event to be tracked
    :list props_fields: model fields to add as props to tracker
    :dict fields_rename: model fields rename. format: { original_field: new_field, ... }

    TODO: move to class decorator
    """

    def outer_wrapper(serializer_create):
        def wrapper(self, validated_data):
            result = serializer_create(self, validated_data)
            props = {
                (fields_rename.get(k) or k): v
                for k, v in validated_data.items()
                if k in props_fields
            }
            analytics.track(self.context["request"].user.slug, event_name, props)
            return result

        return wrapper

    return outer_wrapper


def track_serializer_field_update(
    event_name, props_fields, field_to_track, fields_rename={}
):
    """
    decorator used for event tracking (analytics) on serializer update() calls.
    trigger track only if the specified field_to_track was changed

    :string event_name: name of the event to be tracked
    :list props_fields: model fields to add as props to tracker
    :string field_to_track: model fields to track if changed (`track` will be emitted only if changed)
    :dict fields_rename: model fields rename. format: { original_field: new_field, ... }

    TODO: move to class decorator
    """

    def outer_wrapper(serializer_update):
        def wrapper(self, instance, validated_data):
            validated_field = validated_data.get(field_to_track)
            if validated_field is None or validated_field == getattr(
                instance, field_to_track
            ):
                # dont emit tracker if field was not changed
                return serializer_update(self, instance, validated_data)

            result = serializer_update(self, instance, validated_data)
            props = {}
            for field_name in props_fields:
                field_value = get_nested_obj_attr_value(
                    result, field_name, seperator="__"
                )
                props[fields_rename.get(field_name) or field_name] = field_value

            analytics.track(self.context["request"].user.slug, event_name, props)
            return result

        return wrapper

    return outer_wrapper
