import random
import uuid

from django.db import models

from server.users.models import User
from server.utils.model_fields import PhoneNumberField


def random_slug():
    return uuid.uuid4().hex.upper()[0: random.randint(10, 22)]


class School(models.Model):
    slug = models.CharField(max_length=40, default=random_slug, primary_key=True)
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    address_city = models.CharField(max_length=50)
    zip_city = models.CharField(max_length=15)
    school_code = models.CharField(max_length=15)
    description = models.CharField(max_length=150)
    contact_phone = PhoneNumberField(max_length=15)
    website = models.URLField()
    profile_picture = models.ImageField(null=True, blank=True)
    grade_levels = models.JSONField()


class SchoolMember(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="school_member"
    )
    school = models.ForeignKey(
        School,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="school_member",
    )
