import analytics

from server.utils.helpers import get_nested_obj_attr_value


class _BaseTrackerMixin:
    tracker_on_create_event_name = None
    tracker_on_field_update_event_name = None
    tracker_props_fields = None
    tracker_fields_rename = {}

    def __init__(self, *args, **kwargs):
        self._tracker_props = {}
        self._tracker_user_slug = ""

        if self.tracker_props_fields is None:
            raise AttributeError(
                "tracker_props_fields class attribute must be declared"
            )

        return super().__init__(*args, **kwargs)

    def _tracker_track_creation(self):
        analytics.track(
            self._tracker_user_slug,
            self.tracker_on_create_event_name,
            self._tracker_props,
        )

    def _tracker_track_field_update(self):
        analytics.track(
            self._tracker_user_slug,
            self.tracker_on_field_update_event_name,
            self._tracker_props,
        )

    def _tracker_set_props(self, post_save_obj):
        """
        set the dict of props to send, using the updated/created django object
        """
        for field_name in self.tracker_props_fields:
            field_value = get_nested_obj_attr_value(
                post_save_obj, field_name, seperator="__"
            )
            renamed_field_name = (
                self.tracker_fields_rename.get(field_name) or field_name
            )
            self._tracker_props[renamed_field_name] = field_value


class _BaseCreateTrackerMixin:
    """
    should be used in conjunction with base tracker mixin
    """

    def __init__(self, *args, **kwargs):
        if self.tracker_on_create_event_name is None:
            raise AttributeError(
                "tracker_on_create_event_name class attribute must be decalred"
            )

        return super().__init__(*args, **kwargs)


class _BaseFieldUpdateTrackerMixin:
    """
    should be used in conjunction with base tracker mixin
    """

    # model field to track if changed. i.e., `track` will be emitted only if the field was updated
    tracker_fields_to_track = None

    def __init__(self, *args, **kwargs):
        if self.tracker_fields_to_track is None:
            raise AttributeError(
                "tracker_fields_to_track class attribute must be declared"
            )

        if self.tracker_on_field_update_event_name is None:
            raise AttributeError(
                "tracker_on_field_update_event_name class attribute must be decalred"
            )

        return super().__init__(*args, **kwargs)


class TrackAdminCreateMixin(_BaseCreateTrackerMixin, _BaseTrackerMixin):
    """
    mixin used for event tracking (analytics) on admin panel model object creation.
    should be used with ModelAdmin
    """

    def save_model(self, request, obj, form, change):
        """
        extend ModelAdmin's save_model function
        [https://docs.djangoproject.com/en/3.2/ref/contrib/admin/#django.contrib.admin.ModelAdmin.save_model]
        """
        if not change:
            # it's a newly created object - track it
            self._tracker_set_props(obj)
            self._tracker_user_slug = request.user.slug
            self._tracker_track_creation()
        return super().save_model(request, obj, form, change)


class TrackAdminFieldUpdateMixin(_BaseFieldUpdateTrackerMixin, _BaseTrackerMixin):
    """
    mixin used for event tracking (analytics) when a model object's specific field is updated from Admin Panel
    (e.g. track all `status` field changes in a model, made in admin panel).
    should be used with ModelAdmin
    """

    def save_model(self, request, obj, form, change):
        """
        extend ModelAdmin's save_model function
        [https://docs.djangoproject.com/en/3.2/ref/contrib/admin/#django.contrib.admin.ModelAdmin.save_model]
        """
        if change and any(
            field_name in form.changed_data
            for field_name in self.tracker_fields_to_track
        ):
            # field was updated - track the change
            self._tracker_set_props(obj)
            self._tracker_user_slug = request.user.slug
            self._tracker_track_field_update()

        return super().save_model(request, obj, form, change)


class TrackSerializerCreateMixin(_BaseCreateTrackerMixin, _BaseTrackerMixin):
    """
    mixin used for event tracking (analytics) on serializer create() calls.
    should be used on a serializer
    """

    def create(self, validated_data):
        result = super().create(validated_data)
        self._tracker_set_props(result)
        self._tracker_user_slug = self.context["request"].user.slug
        self._tracker_track_creation()
        return result


class TrackSerializerFieldUpdateMixin(_BaseFieldUpdateTrackerMixin, _BaseTrackerMixin):
    """
    mixin used for event tracking (analytics) when a model object's specific field is updated from serializer
    (e.g. track all `status` field changes in a model from serializer).
    should be used on a serializer
    """

    def _tracker_is_tracked_field_updated(self, instance, validated_data):
        """
        check if at least one tracked field was updated

        params are DRF serializer update's `instance`, `validated_data`:
        [https://www.django-rest-framework.org/tutorial/1-serialization/#creating-a-serializer-class]
        """
        for field_name in self.tracker_fields_to_track:
            if validated_data.get(field_name) != getattr(instance, field_name):
                return True
        return False

    def update(self, instance, validated_data):
        if not self._tracker_is_tracked_field_updated(instance, validated_data):
            # don't emit tracker if no tracked field was not changed
            return super().update(instance, validated_data)

        result = super().update(instance, validated_data)
        self._tracker_set_props(result)
        self._tracker_user_slug = self.context["request"].user.slug
        self._tracker_track_field_update()
        return result
