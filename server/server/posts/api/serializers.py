from rest_framework import serializers

from server.events.models import Event
from server.posts.models import Post, PostImage
from server.users.models import InstructorProfile


class PostImageSerializer(serializers.ModelSerializer):
    post = serializers.SlugRelatedField(
        slug_field="slug",
        queryset=Post.objects.all(),
    )

    class Meta:
        model = PostImage
        fields = [
            "slug",
            "image_url",
            "post",
        ]
        read_only_fields = ["slug"]


class ImageOnlyPostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = ["image_url"]
        read_only_fields = ["image_url"]


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
    author_name = serializers.CharField(source="author.name", read_only=True)
    images = ImageOnlyPostImageSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = [
            "slug",
            "created",
            "event",
            "author",
            "author_name",
            "author_profile_picture",
            "post_content",
            "images",
        ]
        read_only_fields = [
            "slug",
            "created",
            "author",
            "author_profile_picture",
        ]

    def get_author_profile_picture(self, obj):
        return InstructorProfile.objects.get(user=obj.author).profile_picture
