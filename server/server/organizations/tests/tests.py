import os

import pytest
from django.test import override_settings
from rest_framework import status
from rest_framework.test import APIClient

from server.organizations.models import SchoolActivityGroup, SchoolActivityOrder
from server.schools.models import SchoolMember

pytestmark = pytest.mark.django_db
RESET_BASE_URL = os.environ.get("GITPOD_WORKSPACE_URL")[8:]


class TestManageSchoolProgramsView:
    @override_settings(DEBUG=True)
    def test_create(self, school, coordinator, activity):
        url = "/api/manage_school_activity/"
        SchoolMember.objects.create(school=school, user=coordinator)
        client = APIClient()
        client.force_authenticate(user=coordinator)
        post_response = client.post(
            url, {"school": school.slug, "activity": activity.slug}, format="json"
        )
        get_response = client.get(url)

        assert len(get_response.data["results"]) == 1
        assert post_response.status_code == status.HTTP_201_CREATED
        assert get_response.status_code == status.HTTP_200_OK
        assert post_response.data == get_response.data["results"][0]
        assert (
            post_response.data["requested_by"]
            == post_response.data["last_updated_by"]
            == coordinator.slug
        )
        assert post_response.data["status"] == "PENDING_ADMIN_APPROVAL"

    @override_settings(DEBUG=True)
    def test_create_without_member(self, school, school1, coordinator, activity):
        """
        make sure can't create when not a school member
        """
        url = "/api/manage_school_activity/"
        client = APIClient()
        client.force_authenticate(user=coordinator)
        post_response = client.post(
            url, {"school": school.slug, "activity": activity.slug}, format="json"
        )

        SchoolMember.objects.create(school=school1, user=coordinator)
        post_response_2 = client.post(
            url, {"school": school.slug, "activity": activity.slug}, format="json"
        )
        assert post_response.status_code == post_response_2.status_code == 400


class TestConsumerActivityView:
    @override_settings(DEBUG=True)
    def test_consumer_can_view_only_approved_activities(
        self, consumer, school, activity
    ):
        url = "/api/consumer_activities/"
        SchoolMember.objects.create(user=consumer, school=school)

        client = APIClient()
        client.force_authenticate(user=consumer)
        get_response_before_order = client.get(url)

        order = SchoolActivityOrder.objects.create(activity=activity, school=school)
        get_response_after_order_creation = client.get(url)

        order.status = SchoolActivityOrder.Status.APPROVED
        order.save()
        get_response_after_order_approval = client.get(url)

        assert (
            status.HTTP_200_OK
            == get_response_before_order.status_code
            == get_response_after_order_creation.status_code
            == get_response_after_order_approval.status_code
        )
        assert (
            get_response_before_order.data["results"]
            == get_response_after_order_creation.data["results"]
            == []
        )
        assert len(get_response_after_order_approval.data["results"]) == 1

    @override_settings(DEBUG=True)
    def test_consumer_can_view_registration_status(self, consumer, school, activity):
        """
        test if registration status is true if in group, false otherwise
        """
        url = "/api/consumer_activities/"
        SchoolMember.objects.create(user=consumer, school=school)
        activity_order = SchoolActivityOrder.objects.create(
            activity=activity, school=school, status=SchoolActivityOrder.Status.APPROVED
        )
        activity_group = SchoolActivityGroup.objects.create(
            activity_order=activity_order
        )

        client = APIClient()
        client.force_authenticate(user=consumer)
        response_before_consumer_in_group = client.get(url)

        activity_group.consumers.add(consumer)
        response_after_consumer_in_group = client.get(url)

        assert (
            response_before_consumer_in_group.data["results"][0][
                "is_consumer_registered"
            ]
            is False
        )
        assert (
            response_after_consumer_in_group.data["results"][0][
                "is_consumer_registered"
            ]
            is True
        )


class TestConsumerActivityRegisterView:
    @override_settings(
        DEBUG=True,
        RESET_BASE_URL="https://8000-{0}".format(RESET_BASE_URL),
    )
    def test_registeration(self, consumer, school_activity_group):
        url = "/api/consumer_activity_register/"
        activity_slug = school_activity_group.activity_order.activity.slug
        consumer.SchoolMember.school = school_activity_group.activity_order.school
        consumer.save()

        client = APIClient()
        client.force_authenticate(user=consumer)
        response = client.post(url, {"activity_slug": activity_slug})

        assert response.status_code == status.HTTP_201_CREATED
