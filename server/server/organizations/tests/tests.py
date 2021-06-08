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
    uri = "/api/manage_school_activity/"

    @override_settings(DEBUG=True)
    def test_create(self, school, coordinator, activity):
        SchoolMember.objects.create(school=school, user=coordinator)
        client = APIClient()
        client.force_authenticate(user=coordinator)
        post_response = client.post(
            self.uri, {"school": school.slug, "activity": activity.slug}, format="json"
        )
        get_response = client.get(self.uri)

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
        self.uri = "/api/manage_school_activity/"
        client = APIClient()
        client.force_authenticate(user=coordinator)
        post_response = client.post(
            self.uri, {"school": school.slug, "activity": activity.slug}, format="json"
        )

        SchoolMember.objects.create(school=school1, user=coordinator)
        post_response_2 = client.post(
            self.uri, {"school": school.slug, "activity": activity.slug}, format="json"
        )
        assert (
            status.HTTP_400_BAD_REQUEST
            == post_response.status_code
            == post_response_2.status_code
        )


class TestConsumerActivityView:
    uri = "/api/consumer_activities/"

    @override_settings(DEBUG=True)
    def test_consumer_can_view_only_approved_activities(
        self, consumer, school, activity
    ):
        SchoolMember.objects.create(user=consumer, school=school)

        client = APIClient()
        client.force_authenticate(user=consumer)
        get_response_before_order = client.get(self.uri)

        order = SchoolActivityOrder.objects.create(activity=activity, school=school)
        get_response_after_order_creation = client.get(self.uri)

        order.status = SchoolActivityOrder.Status.APPROVED
        order.save()
        get_response_after_order_approval = client.get(self.uri)

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
    def test_consumer_can_view_join_status(self, consumer, school, activity):
        """
        test if join status is true if in group, false otherwise
        """
        SchoolMember.objects.create(user=consumer, school=school)
        activity_order = SchoolActivityOrder.objects.create(
            activity=activity, school=school, status=SchoolActivityOrder.Status.APPROVED
        )
        activity_group = SchoolActivityGroup.objects.create(
            activity_order=activity_order
        )

        client = APIClient()
        client.force_authenticate(user=consumer)
        response_before_consumer_in_group = client.get(self.uri)

        activity_group.consumers.add(consumer)
        response_after_consumer_in_group = client.get(self.uri)

        assert (
            response_before_consumer_in_group.data["results"][0]["is_consumer_joined"]
            is False
        )
        assert (
            response_after_consumer_in_group.data["results"][0]["is_consumer_joined"]
            is True
        )

    @override_settings(
        DEBUG=True,
        RESET_BASE_URL="https://8000-{0}".format(RESET_BASE_URL),
    )
    def test_join_group_action_with_create(self, consumer, school_activity_order):
        """
        test consumer can join to an activity, when there are no groups (i.e., group is created)
        """
        activity_slug = school_activity_order.activity.slug
        SchoolMember.objects.create(user=consumer, school=school_activity_order.school)
        client = APIClient()
        client.force_authenticate(user=consumer)
        action_uri = f"{self.uri}{activity_slug}/join_group/"
        response = client.post(action_uri)
        assert (
            SchoolActivityGroup.objects.get(
                activity_order=school_activity_order,
            ).consumers.all()[0]
            == consumer
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT

    @override_settings(
        DEBUG=True,
        RESET_BASE_URL="https://8000-{0}".format(RESET_BASE_URL),
    )
    def test_join_group_action(self, consumer, school_activity_group):
        """
        test consumer can join to an existing activity group
        """
        school_activity_group.group_type = (
            school_activity_group.GroupTypes.CONTAINER_ONLY,
        )
        school_activity_group.save()
        school_activity_order = school_activity_group.activity_order
        activity_slug = school_activity_order.activity.slug
        SchoolMember.objects.create(user=consumer, school=school_activity_order.school)

        client = APIClient()
        client.force_authenticate(user=consumer)
        action_uri = f"{self.uri}{activity_slug}/join_group/"
        response = client.post(action_uri)
        assert school_activity_group.consumers.all()[0] == consumer
        assert response.status_code == status.HTTP_204_NO_CONTENT
