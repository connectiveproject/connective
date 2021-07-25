from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from server.events.api.views import (
    ConsumerEventFeedbackViewset,
    ConsumerEventViewSet,
    EventViewSet,
)
from server.organizations.api.views import (
    ActivityMediaViewSet,
    ActivityViewSet,
    ConsumerActivityViewSet,
    ManageSchoolActivityViewSet,
    OrganizationViewSet,
    SchoolActivityGroupViewSet,
    VendorActivityViewSet,
)
from server.schools.api.views import SchoolViewSet
from server.users.api.views import (
    ConsumerProfileViewSet,
    CoordinatorProfileViewSet,
    ExportConsumerListViewSet,
    ExportCoordinatorListViewSet,
    InstructorProfileViewSet,
    ManageConsumersViewSet,
    ManageCoordinatorsViewSet,
    ManageInstructorsViewSet,
    ManageVendorsViewSet,
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
router.register(
    "vendor_activities",
    VendorActivityViewSet,
    basename="vendor_activities",
)
router.register("schools", SchoolViewSet, "schools")
router.register("manage_consumers", ManageConsumersViewSet, basename="manage_consumers")
router.register(
    "manage_coordinators", ManageCoordinatorsViewSet, basename="manage_coordinators"
)
router.register(
    "export_consumer_list", ExportConsumerListViewSet, basename="export_consumer_list"
)
router.register(
    "export_coordinator_list",
    ExportCoordinatorListViewSet,
    basename="export_coordinator_list",
)
router.register(
    "manage_instructors", ManageInstructorsViewSet, basename="manage_instructors"
)
router.register("manage_vendors", ManageVendorsViewSet, basename="manage_vendors")
router.register(
    "manage_school_activity",
    ManageSchoolActivityViewSet,
    basename="manage_school_activity",
)
router.register("school_activity_group", SchoolActivityGroupViewSet)
router.register("events", EventViewSet, basename="events")
router.register("consumer_events", ConsumerEventViewSet, basename="consumer_events")
router.register(
    "consumer_event_feedback",
    ConsumerEventFeedbackViewset,
    basename="consumer_event_feedback",
)

app_name = "api"
urlpatterns = router.urls
