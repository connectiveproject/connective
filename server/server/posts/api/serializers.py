from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
    SlugRelatedField,
)

from server.events.models import Event
from server.posts.models import Post
from server.users.models import InstructorProfile


class PostSerializer(ModelSerializer):
    event = SlugRelatedField(
        slug_field="slug",
        queryset=Event.objects.all(),
    )
    author = SlugRelatedField(
        slug_field="slug",
        read_only=True,
    )
    author_profile_picture = SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            "slug",
            "creation_time",
            "event",
            "author",
            "author_profile_picture",
            "post_content",
            "images_b64",
        ]
        read_only_fields = [
            "slug",
            "creation_time",
        ]

    def get_author_profile_picture(self, obj):
        return InstructorProfile.objects.get(user=obj.author).profile_picture
