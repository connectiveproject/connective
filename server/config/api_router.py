from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from server.events.api.views import ConsumerEventViewSet, EventViewSet
from server.organizations.api.views import (
    ActivityMediaViewSet,
    ActivityViewSet,
    ConsumerActivityViewSet,
    ManageSchoolActivityViewSet,
    OrganizationViewSet,
    SchoolActivityGroupViewSet,
)
from server.schools.api.views import SchoolViewSet
from server.users.api.views import (
    ConsumerProfileViewSet,
    CoordinatorProfileViewSet,
    InstructorProfileViewSet,
    ManageConsumersViewSet,
    ManageCoordinatorsViewSet,
    UserViewSet,
    VendorProfileViewSet,
)

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register(
    "consumers_profiles",
    ConsumerProfileViewSet,
    basename="consumers_profiles",
)
router.register(
    "coordinators_profiles",
    CoordinatorProfileViewSet,
    basename="coordinators_profiles",
)
router.register(
    "instructors_profiles",
    InstructorProfileViewSet,
    basename="instructors_profiles",
)
router.register("vendors_profiles", VendorProfileViewSet, basename="vendors_profiles")
router.register("organizations", OrganizationViewSet, basename="organizations")
router.register("activity_media", ActivityMediaViewSet, basename="activity_media")
router.register("activities", ActivityViewSet, basename="activities")
router.register(
    "consumer_activities",
    ConsumerActivityViewSet,
    basename="consumer_activities",
)
router.register("schools", SchoolViewSet, "schools")
router.register("manage_consumers", ManageConsumersViewSet, basename="manage_consumers")
router.register(
    "manage_coordinators", ManageCoordinatorsViewSet, basename="manage_coordinators"
)
router.register("manage_school_activity", ManageSchoolActivityViewSet)
router.register("school_activity_group", SchoolActivityGroupViewSet)
router.register("events", EventViewSet, basename="events")
router.register("consumer_events", ConsumerEventViewSet, basename="consumer_events")

app_name = "api"
urlpatterns = router.urls
