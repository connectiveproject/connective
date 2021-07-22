from django.contrib.auth import get_user_model
from rest_framework import viewsets

from server.posts.api.serializers import PostSerializer
from server.posts.models import Post
from server.utils.permission_classes import (
    AllowConsumerReadOnly,
    AllowCoordinatorReadOnly,
    AllowInstructor,
    AllowSupervisorReadOnly,
    AllowVendorReadOnly,
)


class PostViewSet(viewsets.ModelViewSet):
    permission_classes = [
        AllowConsumerReadOnly,
        AllowInstructor,
        AllowCoordinatorReadOnly,
        AllowSupervisorReadOnly,
        AllowVendorReadOnly,
    ]
    lookup_field = "slug"
    serializer_class = PostSerializer

    def get_queryset(self):
        user = self.request.user

        if user.user_type == get_user_model().Types.CONSUMER:  # student
            # return Post.objects.filter(event__school_group__consumers__contains=user)
            return Post.objects.filter(event__school_group__consumers=user)
        elif user.user_type == get_user_model().Types.INSTRUCTOR:
            # # TODO: db join
            # school_activity_groups = SchoolActivityGroup.objects.filter(
            #     instructor=user,
            # )
            # events = Event.objects.filter(
            #     school_group__in=school_activity_groups,
            # )
            # return Post.objects.filter(
            #     event__in=events,
            # )
            return Post.objects.filter(event__school_group__instructor=user)
        elif user.user_type == get_user_model().Types.COORDINATOR:  # school manager
            return Post.objects.filter(
                event__school_group__activity_order__school__school_member__user=user,
            )
            # schoolMember -> school_activity_order -> school_activity_group
        elif user.user_type == get_user_model().Types.SUPERVISOR:
            return Post.objects.all()
        elif user.user_type == get_user_model().Types.VENDOR:
            return Post.objects.filter(
                event__school_group__activity_order__activity__originization__organization_member__user=user,
            )
        return []

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
        )

    def perform_update(self, serializer):
        serializer.save(
            author=self.request.user,
        )
