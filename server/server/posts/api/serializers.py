from rest_framework.serializers import ModelSerializer, SlugRelatedField

from server.posts.models import Post


class PostSerializer(ModelSerializer):
    event = SlugRelatedField(
        slug_field="slug",
        queryset=Post.objects.all(),
    )
    author = SlugRelatedField(
        slug_field="slug",
        read_only=True,
    )

    class Meta:
        model = Post
        fields = [
            "slug",
            "event",
            "author",
            "post_content",
            "images_b64",
        ]
        read_only_fields = ["slug"]
