import random
import uuid

from django.db import models

from server.users.models import User
from server.utils.model_fields import PhoneNumberField


def random_slug():
    return uuid.uuid4().hex.upper()[0 : random.randint(10, 22)]  # noqa


class School(models.Model):
    slug = models.CharField(max_length=40, default=random_slug, unique=True)
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    address_city = models.CharField(max_length=50)
    zip_city = models.CharField(max_length=15, blank=True)
    school_code = models.CharField(max_length=15)
    description = models.CharField(max_length=150, blank=True)
    contact_phone = PhoneNumberField(max_length=15)
    website = models.URLField(blank=True)
    profile_picture = models.ImageField(null=True, blank=True)
    grade_levels = models.JSONField()
    last_updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="last_updated_by_me_schools",
    )

    def __str__(self):
        return f"{self.name} | {self.address_city} | {self.slug}"


class SchoolMember(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="school_member"
    )
    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        related_name="school_member",
    )

    def __str__(self):
        return f"{self.user.email} | {self.school.name}"
