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
    images = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            "slug",
            "creation_time",
            "event",
            "author",
            "author_name",
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

    def get_images(self, obj):
        request = self.context.get("request")
        return [
            request.build_absolute_uri(img.image_url.url)
            for img in PostImage.objects.filter(post__slug=obj.slug)
        ]
