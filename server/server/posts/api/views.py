from django.contrib.auth import get_user_model
from rest_framework import viewsets

from server.posts.models import Post
from server.posts.api.serializers import PostSerializer

from server.server.events.models import Event
from server.server.organizations.models import SchoolActivityGroup


class PostViewSet(viewsets.ModelViewSet):
    lookup_field = "slug"
    serializer_class = PostSerializer

    def get_queryset(self):
        user = self.request.user

        if user.user_type == get_user_model().Types.CONSUMER:  # student
            pass
        elif user.user_type == get_user_model().Types.INSTRUCTOR:
            return Post.objects.filter(
                event=Event.objects.filter(school_group=
                    SchoolActivityGroup.objects.filter(
                        instructor=user,
                    )
                )
            )
        elif user.user_type == get_user_model().Types.COORDINATOR:  # school manager
            pass
        elif user.user_type == get_user_model().Types.SUPERVISOR:
            return Post.objects.all()

        return []

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
        )

    def perform_update(self, serializer):
        serializer.save(
            author=self.request.user,
        )
