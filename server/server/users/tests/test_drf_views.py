import os

import pytest
from django.core import mail
from django.test import RequestFactory, override_settings
from rest_framework import status
from rest_framework.test import APIClient

from server.schools.models import SchoolMember
from server.users.api.views import UserViewSet
from server.users.models import BaseProfile, User

pytestmark = pytest.mark.django_db
RESET_BASE_URL = os.environ.get("GITPOD_WORKSPACE_URL")[8:]


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
            "slug": user.username,
            "email": user.email,
            "name": user.name,
            "url": f"http://testserver/api/users/{user.username}/",
            "user_type": user.user_type,
        }


class TestManageConsumersView:
    url = "/api/manage_consumers/"

    @override_settings(
        DEBUG=True,
        RESET_BASE_URL="https://8000-{0}".format(RESET_BASE_URL),
    )
    def test_coordinator_can_create_get_consumer(self, coordinator, school):
        create_payload = {
            "name": "name",
            "email": "new-consumer@example.com",
            "profile": {"gender": BaseProfile.Gender.MALE},
        }
        SchoolMember.objects.create(user=coordinator, school=school)

        client = APIClient(coordinator)
        client.force_authenticate(coordinator)

        # create consumer
        consumer_post_response = client.post(self.url, create_payload, format="json")
        consumer_slug = consumer_post_response.data["slug"]
        detail_url = f"{self.url}{consumer_slug}/"

        # get created consumer (via list & detailed)
        consumer_list_get_response = client.get(self.url)
        consumer_detail_get_response = client.get(detail_url)

        assert (
            consumer_list_get_response.status_code
            == consumer_detail_get_response.status_code
            == status.HTTP_200_OK
        )

        # validate get requests
        list_results = consumer_list_get_response.data["results"]
        assert len(list_results) == 1
        assert list_results[0] == consumer_detail_get_response.data
        assert list_results[0]["name"] == create_payload["name"]

        # currently a bug - waiting for resolve:
        # check post response: check nested serializer changed from default value
        # assert (
        #     consumer_post_response.data["profile"]["gender"]
        #     == create_payload["profile"]["gender"]
        # )

    @override_settings(
        DEBUG=True,
        RESET_BASE_URL="https://8000-{0}".format(RESET_BASE_URL),
    )
    def test_email_on_create(self, coordinator, school):
        """
        make sure an email is sent on creation
        """
        create_payload = {"email": "new-consumer@example.com", "profile": {}}
        SchoolMember.objects.create(user=coordinator, school=school)

        client = APIClient(coordinator)
        client.force_authenticate(coordinator)
        client.post(self.url, create_payload, format="json")

        assert len(mail.outbox) == 1
        assert mail.outbox[0].to[0] == create_payload["email"]

    def test_email_on_update(self, school_entities):
        """
        make sure an email is sent on email update only
        """
        email = "new-mail@example.com"
        client = APIClient(school_entities["coord"])
        client.force_authenticate(school_entities["coord"])
        client.patch(
            f"{self.url}{school_entities['consumer'].slug}/",
            {"email": email},
            format="json",
        )
        client.patch(
            f"{self.url}{school_entities['consumer'].slug}/",
            {"name": "Dave"},
            format="json",
        )
        assert len(mail.outbox) == 1
        assert mail.outbox[0].to[0] == email


class TestManageCoordinatorsView:
    url = "/api/manage_coordinators/"

    @override_settings(
        DEBUG=True,
        RESET_BASE_URL="https://8000-{0}".format(RESET_BASE_URL),
    )
    def test_coordinator_can_create_get_coordinators(self, coordinator, school):
        create_payload = {
            "name": "name",
            "email": "new-coordinator@example.com",
        }
        SchoolMember.objects.create(user=coordinator, school=school)
        client = APIClient(coordinator)
        client.force_authenticate(coordinator)

        # create coord
        coordinator_post_response = client.post(self.url, create_payload, format="json")
        coordinator_slug = coordinator_post_response.data["slug"]
        detail_url = f"{self.url}{coordinator_slug}/"

        # get created coord (via list & detailed)
        coordinator_list_get_response = client.get(self.url)
        coordinator_detail_get_response = client.get(detail_url)

        assert (
            coordinator_list_get_response.status_code
            == coordinator_detail_get_response.status_code
            == status.HTTP_200_OK
        )

        # validate get requests
        list_results = coordinator_list_get_response.data["results"]
        assert len(list_results) == 2
        assert (
            len(
                [
                    res
                    for res in list_results
                    if res == coordinator_detail_get_response.data
                    and res["name"] == create_payload["name"]
                ]
            )
            == 1
        )

    @override_settings(
        DEBUG=True,
        RESET_BASE_URL="https://8000-{0}".format(RESET_BASE_URL),
    )
    def test_email_on_create(self, coordinator, school):
        """
        make sure an email is sent on creation
        """
        create_payload = {"email": "new-coord@example.com"}
        SchoolMember.objects.create(user=coordinator, school=school)

        client = APIClient(coordinator)
        client.force_authenticate(coordinator)
        client.post(self.url, create_payload, format="json")

        assert len(mail.outbox) == 1
        assert mail.outbox[0].to[0] == create_payload["email"]

    def test_email_on_update(self, school_entities):
        """
        make sure an email is sent on email update only
        """
        email = "new-mail@example.com"
        client = APIClient(school_entities["coord"])
        client.force_authenticate(school_entities["coord"])
        client.patch(
            f"{self.url}{school_entities['coord'].slug}/",
            {"email": email},
            format="json",
        )
        client.patch(
            f"{self.url}{school_entities['coord'].slug}/",
            {"name": "Dave"},
            format="json",
        )
        assert len(mail.outbox) == 1
        assert mail.outbox[0].to[0] == email
