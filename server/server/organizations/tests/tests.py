import pytest
from rest_framework.test import APIClient

pytestmark = pytest.mark.django_db


class TestManageSchoolProgramsView:
    def test_create(self, school, coordinator, activity):
        url = "/api/manage_school_programs"
        client = APIClient(coordinator)
        client.force_login(coordinator)
        post_response = client.post(url, {school: school.slug, activity: activity.slug})
        get_response = client.get(url)
        post_response_data = post_response.to_json()

        assert len(get_response) == 1
        assert post_response.status_code == get_response.status_code == 200
        assert post_response_data == get_response[0].to_json()
        assert post_response_data.requester == coordinator.slug
        assert post_response_data.status == "pending_admin_approval"
