from unittest.mock import patch

import pytest
from django.conf import settings
from django.urls import reverse
from rest_framework.test import APIClient

from server.organizations.models import SchoolActivityGroup, SchoolActivityOrder
from server.utils.analytics_utils import event

pytestmark = pytest.mark.django_db


class TestTrackerMixins:
    def test_track_serializer_create(self, all_entities):
        """
        check `track` is called on serializer object create, with the correct props
        """
        with patch("analytics.track") as track_mock:
            uri = "/api/school_activity_group/"
            group_data = {
                "name": "group_name",
                "description": "group_desciption",
                "activity_order": all_entities["activity_order"].slug,
            }
            coord = all_entities["coord"]
            client = APIClient()
            client.force_authenticate(user=coord)
            post_response = client.post(
                uri,
                group_data,
                format="json",
                **settings.TEST_API_ADDITIONAL_PARAMS,
            )

            track_mock.assert_called_with(
                coord.slug,
                event.ACTIVITY_GROUP_CREATED,
                {
                    "slug": post_response.data["slug"],
                    "name": post_response.data["name"],
                    "group_type": post_response.data["group_type"],
                    "activity_order_slug": post_response.data["activity_order"],
                },
            )

    def test_track_serializer_field_update(self, all_entities):
        """
        check `track` is called on serializer field update, with the correct props
        """
        with patch("analytics.track") as track_mock:
            coord = all_entities["coord"]
            school_slug = coord.school_member.school.slug
            activity_slug = all_entities["activity"].slug
            uri = f"/api/manage_school_activity/{activity_slug}/"
            order_data = {
                "school": school_slug,
                "status": SchoolActivityOrder.Status.CANCELLED,
            }

            client = APIClient()
            client.force_authenticate(user=coord)
            patch_response = client.patch(
                uri,
                order_data,
                format="json",
            )

            # patch again but don't change the field - should not trigger `track`
            client.patch(
                uri,
                order_data,
                format="json",
            )

            track_mock.assert_called_once_with(
                coord.slug,
                event.ACTIVITY_ORDER_STATUS_UPDATED,
                {
                    "slug": patch_response.data["slug"],
                    "school_slug": school_slug,
                    "activity_slug": activity_slug,
                    "status": patch_response.data["status"],
                },
            )

    def test_track_admin_create(self, admin_client, all_entities):
        """
        check `track` is called on admin panel object create, with the correct props
        """
        with patch("analytics.track") as track_mock:
            uri = reverse("admin:organizations_schoolactivitygroup_add")
            group_data = {
                **settings.TEST_ADDITIONAL_DATA,
                **{
                    "slug": "J123LKASDKAASDK2",
                    "name": "J123LKASDKAASDK2",
                    "description": "group_desciption",
                    "activity_order": all_entities["activity_order"].pk,
                    "group_type": SchoolActivityGroup.GroupTypes.DEFAULT,
                },
            }
            admin_client.post(
                uri,
                data=group_data,
                **settings.TEST_API_ADDITIONAL_PARAMS,
            )
            created_obj = SchoolActivityGroup.objects.get(name=group_data["name"])
            track_mock.assert_called_with(
                "admin",
                event.ACTIVITY_GROUP_CREATED,
                {
                    "slug": created_obj.slug,
                    "name": created_obj.name,
                    "group_type": created_obj.group_type,
                    "activity_order_slug": created_obj.activity_order.slug,
                },
            )

    def test_track_admin_field_update(self, admin_client, all_entities):
        """
        check `track` is called on admin panel field update, with the correct props
        """
        with patch("analytics.track") as track_mock:
            order = all_entities["activity_order"]
            uri = reverse(
                "admin:organizations_schoolactivityorder_change",
                kwargs={"object_id": order.pk},
            )

            order_data = {
                **settings.TEST_ADDITIONAL_DATA,
                **{
                    "slug": order.slug,
                    "school": order.school.pk,
                    "activity": order.activity.pk,
                    "status": SchoolActivityOrder.Status.CANCELLED,
                },
            }

            admin_client.post(
                uri,
                data=order_data,
                **settings.TEST_API_ADDITIONAL_PARAMS,
            )

            # patch again but don't change the field - should not trigger `track`
            admin_client.post(
                uri,
                data=order_data,
                **settings.TEST_API_ADDITIONAL_PARAMS,
            )

            updated_obj = SchoolActivityOrder.objects.get(slug=order_data["slug"])
            track_mock.assert_called_once_with(
                "admin",
                event.ACTIVITY_ORDER_STATUS_UPDATED,
                {
                    "slug": updated_obj.slug,
                    "school_slug": updated_obj.school.slug,
                    "activity_slug": updated_obj.activity.slug,
                    "status": updated_obj.status,
                },
            )
