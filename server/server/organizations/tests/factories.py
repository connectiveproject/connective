from factory import Faker, SubFactory
from factory.django import DjangoModelFactory

from server.organizations.models import Activity, Organization


class OrganizationFactory(DjangoModelFactory):
    email = Faker("email")
    description = "description"
    website_url = "https://org.com"
    name = "Organization Name"
    goal = "Goal"
    year_founded = "2005"
    status = "status"
    target_audience = [1, 2, 3, 4, 5, 6]
    number_of_employees = 100
    number_of_members = 200
    number_of_volunteers = 30
    location_lon = 32.109333
    location_lat = 34.855499
    address_city = "city"
    address_street = "addr"
    address_house_num = "13"
    address_zipcode = "550202"
    cities = {}
    districts = {}
    union_type = "union type"

    class Meta:
        model = Organization


class ActivityFactory(DjangoModelFactory):
    name = "Activity Name"
    target_audience = [1, 2, 3]
    domain = "Domain"
    originization = SubFactory(OrganizationFactory)
    description = "Activity Description"
    contact_name = "John Smith"
    logo = None
    phone_number = "0521234567"

    class Meta:
        model = Activity
