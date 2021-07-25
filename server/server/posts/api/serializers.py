from rest_framework import serializers

from server.events.models import Event
from server.posts.models import Post
from server.users.models import InstructorProfile


class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            "slug",
            "image_url",
            "post",
        ]
        read_only_fields = ["slug"]


class PostSerializer(serializers.ModelSerializer):
    event = serializers.SlugRelatedField(
        slug_field="slug",
        queryset=Event.objects.all(),
    )
    author = serializers.SlugRelatedField(
        slug_field="slug",
        read_only=True,
    )
    author_profile_picture = serializers.SerializerMethodField()
    images = PostImageSerializer(many=True, required=False, allow_null=True)

    class Meta:
        model = Post
        fields = [
            "slug",
            "creation_time",
            "event",
            "author",
            "author_profile_picture",
            "post_content",
            "images",
        ]
        read_only_fields = [
            "slug",
            "creation_time",
            "author",
            "author_profile_picture",
        ]

    def get_author_profile_picture(self, obj):
        return InstructorProfile.objects.get(user=obj.author).profile_picture
