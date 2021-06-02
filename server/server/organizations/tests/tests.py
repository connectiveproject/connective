import pytest
from rest_framework.test import APIClient

from server.schools.models import SchoolMember

pytestmark = pytest.mark.django_db


class TestManageSchoolProgramsView:
    def test_create(self, school, coordinator, activity):
        url = "/api/manage_school_activity/"
        client = APIClient()
        client.force_authenticate(user=coordinator)
        post_response = client.post(
            url, {"school": school.slug, "activity": activity.slug}, format="json"
        )
        get_response = client.get(url)
        post_response_data = post_response.to_json()

        assert len(get_response) == 1
        assert post_response.status_code == get_response.status_code == 200
        assert post_response_data == get_response[0].to_json()
        assert (
            post_response_data["requested_by"]
            == post_response_data["last_updated_by"]
            == coordinator.slug
        )
        assert post_response_data["status"] == "pending_admin_approval"

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
