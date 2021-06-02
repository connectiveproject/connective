import pytest
from django.test import override_settings
from rest_framework.test import APIClient

from server.schools.models import SchoolMember

pytestmark = pytest.mark.django_db


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
        assert post_response.status_code == 201
        assert get_response.status_code == 200
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
