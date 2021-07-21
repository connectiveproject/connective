from rest_framework.serializers import ModelSerializer

from server.posts.models import Post


class PostSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = [
            "slug",
            "event",
            "author",
            "post_content",
            "images",
        ]
        read_only_fields = ["slug"]
