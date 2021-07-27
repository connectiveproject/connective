import pytest
from rest_framework.test import APIClient

from server.schools.models import School, SchoolMember
from server.users.models import Coordinator

pytestmark = pytest.mark.django_db


class TestSchoolViewSet:
    def test_school_endpoint(self):
        """
        test school list & school details (specific school) GET requests.
        authorization: see users can't see unrelated schools
        integrity: see the data is as it should be
        """
        school_data = {
            "address": "123 foo foo",
            "address_city": "city",
            "address_zipcode": "1111111111111",
            "school_code": "1111111111111",
            "description": "A SCHOOL",
            "contact_phone": "1111111111111",
            "website": "http://example.com",
            "profile_picture": None,
            "grade_levels": [1, 2, 3],
        }
        school1_data = {"name": "school1", **school_data}
        school2_data = {"name": "school2", **school_data}

        user1 = Coordinator.objects.create(
            email="user1@example.com",
            password="password1",
        )
        user2 = Coordinator.objects.create(
            email="user2@example.com",
            password="password2",
        )

        client = APIClient(user1)
        client.force_authenticate(user1)

        # query API before adding schools
        list_response_no_schools = client.get("/api/schools/")

        school1 = School.objects.create(**school1_data)
        school2 = School.objects.create(**school2_data)

        SchoolMember.objects.create(user=user1, school=school1)
        SchoolMember.objects.create(user=user2, school=school2)

        # query API after adding schools
        list_response_single_school = client.get("/api/schools/")

        # check user can see exactly the schools it should
        assert not list_response_no_schools.data["results"]
        assert len(list_response_single_school.data["results"]) == 1

        # check the data itself from a specific school & school list data
        school1_slug = list_response_single_school.data["results"][0]["slug"]
        school1_data["slug"] = school1_slug
        detail_response = client.get(f"/api/schools/{school1_slug}/")
        assert (
            school1_data
            == list_response_single_school.data["results"][0]
            == detail_response.data
        )
