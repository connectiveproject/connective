from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from server.organizations.api.views import (
    ActivityMediaViewSet,
    ActivityViewSet,
    OrganizationViewSet,
)
from server.users.api.views import UserViewSet
from server.schools.api.views import SchoolViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register("schools", SchoolViewSet, "schools")
router.register("organizations", OrganizationViewSet, basename="organizations")
router.register("activity_media", ActivityMediaViewSet, basename="activity_media")
router.register("activities", ActivityViewSet, basename="activities")

app_name = "api"
urlpatterns = router.urls
