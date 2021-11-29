from contextlib import suppress
from datetime import datetime, timedelta

import pytest
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient

from server.events.models import Event, EventOrder

pytestmark = pytest.mark.django_db

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


class TestEventOrderModel:
    def test_end_time_validator(self):
        order = EventOrder(
            start_time=tomorrow,
            end_time=today,
        )
        with suppress(ValidationError):
            order.full_clean()
            assert False


class TestEventView:
    uri = "/api/events/"

    def is_event_exist_in_response(response, event_slug):
        for event in response.data["results"]:
            if event["slug"] == event_slug:
                return True
        return False

    def test_end_time_validator(self, all_entities):
        client = APIClient()
        client.force_authenticate(user=all_entities["coord"])
        post_response = client.post(
            self.uri,
            {
                "start_time": tomorrow,
                "end_time": today,
                "consumers": [],
                "school_group": all_entities["activity_group"].slug,
                **settings.TEST_API_ADDITIONAL_PARAMS,
            },
            format="json",
        )
        assert post_response.status_code == status.HTTP_400_BAD_REQUEST
        assert "end_time" in post_response.data

    def test_create_event(self, all_entities):
        coord = all_entities["coord"]
        payload = {
            "start_time": today,
            "end_time": tomorrow,
            "consumers": [all_entities["consumer"].slug],
            "school_group": all_entities["activity_group"].slug,
        }

        client = APIClient()
        client.force_authenticate(user=coord)

        post_response = client.post(
            self.uri, payload, format="json", **settings.TEST_API_ADDITIONAL_PARAMS
        )
        get_response = client.get(self.uri, **settings.TEST_API_ADDITIONAL_PARAMS)

        assert post_response.status_code == status.HTTP_201_CREATED
        assert get_response.status_code == status.HTTP_200_OK
        assert post_response.data == dict(get_response.data["results"][-1])
        assert post_response.data["consumers"] == payload["consumers"]
        assert post_response.data["school_group"] == payload["school_group"]

    def get_request_additional_params(query_string):
        settings_params = settings.TEST_API_ADDITIONAL_PARAMS.copy()
        settings_query_params = settings_params.pop("QUERY_STRING")
        query_string_final = f"{query_string}&{settings_query_params}"
        result = {"QUERY_STRING": query_string_final}
        result.update(settings_params)
        return result

    def test_canceled_event(self, all_entities):
        coord = all_entities["coord"]
        create_payload = {
            "start_time": today,
            "end_time": tomorrow,
            "consumers": [all_entities["consumer"].slug],
            "school_group": all_entities["activity_group"].slug,
        }

        client = APIClient()
        client.force_authenticate(user=coord)

        post_response = client.post(
            self.uri,
            create_payload,
            format="json",
            **settings.TEST_API_ADDITIONAL_PARAMS,
        )
        assert post_response.status_code == status.HTTP_201_CREATED

        slug = post_response.data["slug"]
        single_event_uri = f"{self.uri}{slug}/"
        get_response = client.get(
            single_event_uri, **settings.TEST_API_ADDITIONAL_PARAMS
        )
        assert get_response.status_code == status.HTTP_200_OK
        assert get_response.data["is_canceled"] is False

        get_all_events_uri = self.uri
        assert TestEventView.is_event_exist_in_response(
            client.get(get_all_events_uri, **settings.TEST_API_ADDITIONAL_PARAMS), slug
        )
        assert TestEventView.is_event_exist_in_response(
            client.get(
                get_all_events_uri,
                **TestEventView.get_request_additional_params("is_canceled=false"),
            ),
            slug,
        )

        assert not TestEventView.is_event_exist_in_response(
            client.get(
                get_all_events_uri,
                **TestEventView.get_request_additional_params("is_canceled=true"),
            ),
            slug,
        )
        patch_payload = {"is_canceled": True}
        client.patch(
            single_event_uri,
            patch_payload,
            format="json",
            **settings.TEST_API_ADDITIONAL_PARAMS,
        )
        get_response = client.get(
            single_event_uri, **settings.TEST_API_ADDITIONAL_PARAMS
        )
        assert get_response.data["is_canceled"]
        assert TestEventView.is_event_exist_in_response(
            client.get(get_all_events_uri, **settings.TEST_API_ADDITIONAL_PARAMS), slug
        )
        assert not TestEventView.is_event_exist_in_response(
            client.get(
                get_all_events_uri,
                **TestEventView.get_request_additional_params("is_canceled=false"),
            ),
            slug,
        )
        assert TestEventView.is_event_exist_in_response(
            client.get(
                get_all_events_uri,
                **TestEventView.get_request_additional_params("is_canceled=true"),
            ),
            slug,
        )


class TestEventOrderSignals:
    def test_event_orders_signals(self, all_entities):
        """
        test auto create/delete of events after order create/cancel
        """
        # create orders:
        order_pending_approval = EventOrder.objects.create(
            status=EventOrder.Status.PENDING_APPROVAL,
            recurrence=EventOrder.Recurrence.ONE_TIME,
            school_group=all_entities["activity_group"],
            start_time=today,
            end_time=tomorrow,
        )
        order_onetime = EventOrder.objects.create(
            status=EventOrder.Status.APPROVED,
            recurrence=EventOrder.Recurrence.ONE_TIME,
            school_group=all_entities["activity_group"],
            start_time=today,
            end_time=tomorrow,
        )
        events_count_1 = Event.objects.filter(
            event_order__in=[order_pending_approval, order_onetime]
        ).count()

        order_weekly = EventOrder.objects.create(
            status=EventOrder.Status.APPROVED,
            recurrence=EventOrder.Recurrence.WEEKLY,
            school_group=all_entities["activity_group"],
            start_time=today,
            end_time=tomorrow,
        )
        events_count_53 = Event.objects.filter(
            event_order__in=[order_pending_approval, order_onetime, order_weekly]
        ).count()

        # cancel orders:
        order_onetime.status = EventOrder.Status.CANCELLED
        order_onetime.save()
        events_count_52 = Event.objects.filter(
            event_order__in=[order_pending_approval, order_onetime, order_weekly]
        ).count()

        order_weekly.status = EventOrder.Status.CANCELLED
        order_weekly.save()
        events_count_0 = Event.objects.filter(
            event_order__in=[order_pending_approval, order_onetime, order_weekly]
        ).count()

        assert events_count_0 == 0
        assert events_count_1 == 1
        assert events_count_52 == 52
        assert events_count_53 == 53


class TestEventOrderView:
    uri = "/api/event_order/"

    def test_create_event_order(self, all_entities):
        coord = all_entities["coord"]
        order_data = {
            "start_time": today,
            "end_time": tomorrow,
            "school_group": all_entities["activity_group"].slug,
            "recurrence": EventOrder.Recurrence.WEEKLY,
            "status": EventOrder.Status.APPROVED,
        }
        client = APIClient()
        client.force_authenticate(user=coord)
        post_response = client.post(
            self.uri,
            order_data,
            format="json",
            **settings.TEST_API_ADDITIONAL_PARAMS,
        )
        get_response = client.get(self.uri, **settings.TEST_API_ADDITIONAL_PARAMS)
        assert post_response.status_code == status.HTTP_201_CREATED
        assert get_response.status_code == status.HTTP_200_OK
        assert post_response.data == dict(get_response.data["results"][-1])
