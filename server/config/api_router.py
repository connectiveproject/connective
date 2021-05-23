from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from server.users.api.views import UserViewSet
from server.schools.api.views import SchoolViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register("schools", SchoolViewSet, "schools")


app_name = "api"
urlpatterns = router.urls
