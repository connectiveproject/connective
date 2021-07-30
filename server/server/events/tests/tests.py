from contextlib import suppress
from datetime import datetime, timedelta

import pytest
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
            self.uri,
            payload,
            format="json",
        )
        get_response = client.get(self.uri)

        assert post_response.status_code == status.HTTP_201_CREATED
        assert get_response.status_code == status.HTTP_200_OK
        assert post_response.data == dict(get_response.data["results"][-1])
        assert post_response.data["consumers"] == payload["consumers"]
        assert post_response.data["school_group"] == payload["school_group"]


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
        events_count_55 = Event.objects.filter(
            event_order__in=[order_pending_approval, order_onetime, order_weekly]
        ).count()

        # cancel orders:
        order_onetime.status = EventOrder.Status.CANCELLED
        order_onetime.save()
        events_count_54 = Event.objects.filter(
            event_order__in=[order_pending_approval, order_onetime, order_weekly]
        ).count()

        order_weekly.status = EventOrder.Status.CANCELLED
        order_weekly.save()
        events_count_0 = Event.objects.filter(
            event_order__in=[order_pending_approval, order_onetime, order_weekly]
        ).count()

        assert events_count_0 == 0
        assert events_count_1 == 1
        assert events_count_54 == 54
        assert events_count_55 == 55


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
        )
        get_response = client.get(self.uri)
        assert post_response.status_code == status.HTTP_201_CREATED
        assert get_response.status_code == status.HTTP_200_OK
        assert post_response.data == dict(get_response.data["results"][-1])
