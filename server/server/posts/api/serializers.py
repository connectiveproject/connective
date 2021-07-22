from rest_framework.serializers import ModelSerializer, SlugRelatedField

from server.posts.models import Post
from server.events.models import Event


class PostSerializer(ModelSerializer):
    event = SlugRelatedField(
        slug_field="slug",
        queryset=Event.objects.all(),
    )
    author = SlugRelatedField(
        slug_field="slug",
        read_only=True,
    )

    class Meta:
        model = Post
        fields = [
            "slug",
            "creation_time",
            "event",
            "author",
            "post_content",
            "images_b64",
        ]
        read_only_fields = [
            "slug",
            "creation_time",
        ]
