import pytest
from django.test import RequestFactory
from rest_framework.test import APIClient

from server.schools.models import SchoolMember
from server.users.api.views import UserViewSet
from server.users.models import BaseProfile, User

pytestmark = pytest.mark.django_db


class TestUserViewSet:
    def test_get_queryset(self, user: User, rf: RequestFactory):
        view = UserViewSet()
        request = rf.get("/fake-url/")
        request.user = user

        view.request = request

        assert user in view.get_queryset()

    def test_me(self, user: User, rf: RequestFactory):
        view = UserViewSet()
        request = rf.get("/fake-url/")
        request.user = user

        view.request = request

        response = view.me(request)

        assert response.data == {
            "username": user.username,
            "name": user.name,
            "url": f"http://testserver/api/users/{user.username}/",
        }


class TestManageConsumersView:
    def test_crud(self, coordinator, school):
        """
        make sure coordinator can read & create & delete & update a consumer
        """
        # set up
        url = "/api/manage_consumers/"
        payload_format = "json"
        create_payload = {
            "name": "name",
            "email": "new-consumer@example.com",
            "profile": {"gender": BaseProfile.Gender.MALE},
        }
        # update_payload = {
        #     "name": "new-name",
        #     "profile": {"gender": BaseProfile.Gender.FEMALE},
        # }

        SchoolMember.objects.create(user=coordinator, school=school)
        client = APIClient(coordinator)
        client.force_login(coordinator)

        # create consumer
        consumer_post_response = client.post(url, create_payload, format=payload_format)
        consumer_slug = consumer_post_response.to_json().slug
        detail_url = f"{url}{consumer_slug}"

        # get created consumer (via list & detailed)
        consumer_list_get_response = client.get(url)
        consumer_detail_get_response = client.get(detail_url)

        # update consumer
        # consumer_update_response = client.patch(
        #     detail_url, update_payload, format=payload_format
        # )
        # consumer_after_update_response = client.get(detail_url)

        # status codes
        assert (
            consumer_list_get_response.status_code
            == consumer_detail_get_response.status_code
            == 200
        )

        # check nested data changed from default value
        assert (
            consumer_post_response.to_json["profile"]["gender"]
            == create_payload["profile"]["gender"]
        )

        # check list & detailed get requests
        assert len(consumer_list_get_response.to_json()) == 1
        assert (
            consumer_list_get_response.to_json()[0]
            == consumer_detail_get_response.to_json()
        )
        assert consumer_list_get_response.to_json()[0]["name"] == create_payload["name"]

        # remaining - update
        assert False

    def test_email_on_create(self, user: User, rf: RequestFactory):
        """
        make sure an email is sent on creation
        """
        assert False

    def test_bulk_create(self, user: User, rf: RequestFactory):
        """
        make sure coordinator can bulk-create
        """
        assert False

    def test_create_permissions(self, user: User, rf: RequestFactory):
        """
        make sure non-coordinators can't create
        """
        assert False
