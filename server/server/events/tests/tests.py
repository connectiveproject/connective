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
        import ipdb

        ipdb.set_trace()
        post_response = client.post(
            self.uri,
            {
                "start_time": tomorrow,
                "end_time": today,
            },
            format="json",
        )
        assert post_response.status_code == status.HTTP_400_BAD_REQUEST
        assert post_response["data"]["results"][0] == {
            "end_time": "end time must occur after start time"
        }

    def test_create_event(self, coordinator, consumer):
        # client = APIClient()
        # post_response = client.post(
        #     self.uri,
        #     {
        #         "start_time": today,
        #         "end_time": tomorrow,
        #         "consumers": [consumer.slug],
        #         guide: "David",
        #     },
        #     format="json",
        # )

        # client.force_authenticate(user=coordinator)
        # get_response = client.get(self.uri)
        assert False
