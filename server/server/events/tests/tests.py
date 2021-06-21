import os
from contextlib import suppress
from datetime import datetime, timedelta

import pytest
from django.core.exceptions import ValidationError
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient

from server.events.models import Event

pytestmark = pytest.mark.django_db
RESET_BASE_URL = os.environ.get("GITPOD_WORKSPACE_URL")[8:]

today = datetime.now(tz=timezone.utc)
tomorrow = datetime.now(tz=timezone.utc) + timedelta(days=1)


class TestEventModel:
    def test_end_time_validator(self):
        event = Event(
            start_time=tomorrow,
            end_time=today,
        )
        with suppress(ValidationError):
            event.full_clean()
            assert False


class TestEventView:
    uri = "/api/events/"

    def test_end_time_validator(self, coordinator):
        client = APIClient()
        client.force_authenticate(user=coordinator)
        post_response = client.post(
            self.uri,
            {
                "start_time": tomorrow,
                "end_time": today,
            },
            format="json",
        )
        assert post_response.status_code == status.HTTP_400_BAD_REQUEST
        assert "end_time" in post_response.data

    def test_create_event(self, school_entities):
        coord = school_entities["coord"]
        payload = {
            "start_time": today,
            "end_time": tomorrow,
            "consumers": [school_entities["consumer"].pk],
            "school_group": school_entities["activity_group"].pk,
        }

        client = APIClient()
        client.force_authenticate(user=coord)

        post_response = client.post(
            self.uri,
            payload,
            format="json",
        )
        get_response = client.get(self.uri)

        assert post_response.status_code == status.HTTP_201_CREATED
        assert get_response.status_code == status.HTTP_200_OK
        assert post_response.data == dict(get_response.data["results"][0])
        assert post_response.data["consumers"] == payload["consumers"]
        assert post_response.data["school_group"] == payload["school_group"]
