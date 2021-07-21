from rest_framework import viewsets

from server.posts.models import Post
from server.posts.api.serializers import PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    lookup_field = "slug"
    serializer_class = PostSerializer
    queryset = Post.objects.all()
