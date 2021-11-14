import pytest
from django.conf import settings
from django.urls import reverse

from server.users.models import User

pytestmark = pytest.mark.django_db


class TestUserAdmin:
    def test_changelist(self, admin_client):
        url = reverse("admin:users_user_changelist")
        response = admin_client.get(url, **settings.TEST_API_ADDITIONAL_PARAMS)
        assert response.status_code == 200

    def test_search(self, admin_client):
        url = reverse("admin:users_user_changelist")
        response = admin_client.get(
            url, data={"q": "test"}, **settings.TEST_API_ADDITIONAL_PARAMS
        )
        assert response.status_code == 200

    def test_add(self, admin_client):
        url = reverse("admin:users_user_add")
        response = admin_client.get(url, **settings.TEST_API_ADDITIONAL_PARAMS)
        assert response.status_code == 200

        response = admin_client.post(
            url,
            data={
                **settings.TEST_ADDITIONAL_DATA,
                **{
                    "email": "test@example.com",
                    "password1": "My_R@ndom-P@ssw0rd",
                    "password2": "My_R@ndom-P@ssw0rd",
                },
            },
            **settings.TEST_API_ADDITIONAL_PARAMS,
        )
        assert response.status_code == 302
        assert User.objects.filter(email="test@example.com").exists()

    def test_view_user(self, admin_client):
        user = User.objects.get(username="admin")
        url = reverse("admin:users_user_change", kwargs={"object_id": user.pk})
        response = admin_client.get(url, **settings.TEST_API_ADDITIONAL_PARAMS)
        assert response.status_code == 200
