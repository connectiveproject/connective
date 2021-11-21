import pytest
from django.conf import settings
from rest_framework import status
from rest_framework.test import APIClient

pytestmark = pytest.mark.django_db


class TestPostView:
    uri = "/api/posts/"

    def test_create_post(self, all_entities):
        post_data = {
            "event": all_entities["event"].slug,
            "post_content": "I'm a post.",
        }
        client = APIClient()
        client.force_authenticate(user=all_entities["instructor"])
        post_response = client.post(
            self.uri,
            post_data,
            format="json",
            **settings.TEST_API_ADDITIONAL_PARAMS,
        )
        get_response = client.get(self.uri, **settings.TEST_API_ADDITIONAL_PARAMS)

        assert post_response.status_code == status.HTTP_201_CREATED
        assert get_response.status_code == status.HTTP_200_OK
        assert (
            all_entities["instructor"].slug
            == get_response.data["results"][-1]["author"]
            == post_response.data["author"]
        )
