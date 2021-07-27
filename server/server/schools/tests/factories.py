import random

from factory.django import DjangoModelFactory

from server.schools.models import School


class SchoolFactory(DjangoModelFactory):
    name = "School Name"
    address = "Shinkin 87"
    address_city = "Tel Aviv"
    address_zipcode = "0564665"
    school_code = str(random.randint(10000, 99999))
    description = "School description"
    contact_phone = "0521234567"
    website = "https://school.com"
    profile_picture = None
    grade_levels = [1, 2, 3, 4, 5, 6]

    class Meta:
        model = School
