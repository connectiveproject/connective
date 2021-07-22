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
    zip_city = models.CharField(max_length=15)
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


class ImportedSchool(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    address_city = models.CharField(max_length=50)
    school_code = models.IntegerField(unique=True)
    grade_levels = models.JSONField()
    longtitude = models.FloatField()
    latitude = models.FloatField()
    region = models.CharField(max_length=50)
    status = models.CharField(max_length=50)
    boys = models.IntegerField()
    girls = models.IntegerField()
    male_teachers = models.IntegerField()
    female_teachers = models.IntegerField()
    migzar = models.CharField(null=True, blank=True, max_length=50)
    school_type = models.CharField(null=True, blank=True, max_length=50)
    school_stages = models.CharField(null=True, blank=True, max_length=50)
    authority_city = models.CharField(null=True, blank=True, max_length=50)
    is_bagrut = models.BooleanField()
    immigrants_percent = models.FloatField(null=True, blank=True)
    tech_students_percent = models.FloatField(null=True, blank=True)
    tech_diploma_eligible_percent = models.FloatField(null=True, blank=True)
    special_education_percent = models.FloatField(null=True, blank=True)
    social_economic_status = models.IntegerField(null=True, blank=True)
    decile_tipuah_hativa_benaim = models.IntegerField(null=True, blank=True)
    decile_tipuah_hativa_eliona = models.IntegerField(null=True, blank=True)
    decile_tipuah_yesodi = models.IntegerField(null=True, blank=True)
    ivhun_percent = models.FloatField(null=True, blank=True)
    boys_army_enlist_rate = models.FloatField(null=True, blank=True)
    girls_army_enlist_rate = models.FloatField(null=True, blank=True)
    hatmada_percent = models.FloatField(null=True, blank=True)
    drop_rate = models.FloatField(null=True, blank=True)
    bagrut_eligible_percent = models.FloatField(null=True, blank=True)
    bagrut_excelent_eligible_percent = models.FloatField(null=True, blank=True)
    bagrut_english_5u_percent = models.FloatField(null=True, blank=True)
    bagrut_math_5u_percent = models.FloatField(null=True, blank=True)
    last_updated = models.DateTimeField()

    def __str__(self):
        return f"{self.name} | {self.address_city} | {self.school_code}"


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
