from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from server.organizations.api.views import (
    ActivityMediaViewSet,
    ActivityViewSet,
    OrganizationViewSet,
)
from server.schools.api.views import SchoolViewSet
from server.users.api.views import (
    ConsumerProfileViewSet,
    CoordinatorProfileViewSet,
    UserViewSet,
    VendorProfileViewSet,
)

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register(
    "consumers_profiles", ConsumerProfileViewSet, basename="consumers_profiles"
)
router.register(
    "coordinators_profiles", CoordinatorProfileViewSet, basename="coordinators_profiles"
)
router.register("vendors_profiles", VendorProfileViewSet, basename="vendors_profiles")
router.register("organizations", OrganizationViewSet, basename="organizations")
router.register("activity_media", ActivityMediaViewSet, basename="activity_medeas")
router.register("activities", ActivityViewSet, basename="activities")
router.register("schools", SchoolViewSet, "schools")


app_name = "api"
urlpatterns = router.urls
