import analytics

from server.utils.helpers import get_nested_obj_attr_value


class GenericTrackerMixin:
    """
    :string event_name: event name to send on `track` func
    :list props_fields: model fields to add as props to `track`
    :dict fields_rename: model fields rename in props. format: { original_field_name: new_field_name, ... }
    """

    def __init__(self, event_name, props_fields, fields_rename={}):
        self.event_name = event_name
        self.props_fields = props_fields
        self.fields_rename = fields_rename
        self.props = {}
        self.user_slug = ""

    def __call__(self, decorated_func):
        def wrapper(decorated_self, *args, **kwargs):
            # logic before func goes here
            result = decorated_func(decorated_self, *args, **kwargs)
            # logic after func goes here
            self.set_props(result)
            self.track()
            return result

        return wrapper

    def set_props(self, post_save_obj):
        for field_name in self.props_fields:
            field_value = get_nested_obj_attr_value(
                post_save_obj, field_name, seperator="__"
            )
            self.props[self.fields_rename.get(field_name) or field_name] = field_value

    def track(self):
        analytics.track(self.user_slug, self.event_name, self.props)


class TrackAdminCreate(GenericTrackerMixin):
    """
    decorator used for event tracking (analytics) on admin panel model object update

    should be placed on ModelAdmin's save_model()
    [https://docs.djangoproject.com/en/3.2/ref/contrib/admin/#django.contrib.admin.ModelAdmin.save_model]
    """

    def __call__(self, decorated_func):
        def wrapper(decorated_self, request, obj, form, change):
            if not change:
                # it's a newly created object
                self.set_props(obj)
                self.user_slug = request.user.slug
                self.track()

            return decorated_func(decorated_self, request, obj, form, change)

        return wrapper


class TrackAdminFieldUpdate(GenericTrackerMixin):
    """
    decorator used for event tracking (analytics) on admin panel model object creation
    trigger track only if the specified field_to_track was changed

    should be placed on ModelAdmin's save_model()
    [https://docs.djangoproject.com/en/3.2/ref/contrib/admin/#django.contrib.admin.ModelAdmin.save_model]

    :string field_to_track: model field to track if changed. i.e., `track` will be emitted only if the field was updated
    """

    def __init__(self, event_name, props_fields, field_to_track, fields_rename={}):
        super().__init__(event_name, props_fields, fields_rename)
        self.field_to_track = field_to_track

    def __call__(self, decorated_func):
        def wrapper(decorated_self, request, obj, form, change):
            if change and self.field_to_track in form.changed_data:
                # field was updated
                self.set_props(obj)
                self.user_slug = request.user.slug
                self.track()

            return decorated_func(decorated_self, request, obj, form, change)

        return wrapper


class TrackSerializerCreate(GenericTrackerMixin):
    """
    decorator used for event tracking (analytics) on serializer create() calls

    should be placed on serializer's create()
    """

    def __call__(self, decorated_func):
        def wrapper(decorated_self, validated_data):
            result = decorated_func(decorated_self, validated_data)
            self.set_props(result)
            self.user_slug = decorated_self.context["request"].user.slug
            self.track()
            return result

        return wrapper


class TrackSerializerFieldUpdate(GenericTrackerMixin):
    """
    decorator used for event tracking (analytics) on serializer update() calls.
    trigger track only if the specified field_to_track was changed

    should be placed on serializer's update()

    :string field_to_track: model field to track if changed. i.e., `track` will be emitted only if the field was updated
    """

    def __init__(self, event_name, props_fields, field_to_track, fields_rename={}):
        super().__init__(event_name, props_fields, fields_rename)
        self.field_to_track = field_to_track

    def __call__(self, decorated_func):
        def wrapper(decorated_self, instance, validated_data):
            validated_field = validated_data.get(self.field_to_track)
            if validated_field is None or validated_field == getattr(
                instance, self.field_to_track
            ):
                # dont emit tracker if field was not changed
                return decorated_func(decorated_self, instance, validated_data)

            result = decorated_func(decorated_self, instance, validated_data)
            self.set_props(result)
            self.user_slug = decorated_self.context["request"].user.slug
            self.track()
            return result

        return wrapper
