from datetime import datetime, timedelta

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import IntegrityError
from django.utils import timezone

from server.events.models import Event, EventOrder
from server.organizations.models import (
    Activity,
    Organization,
    OrganizationMember,
    SchoolActivityGroup,
    SchoolActivityOrder,
)
from server.schools.models import School, SchoolMember
from server.users.models import Consumer, Coordinator, Instructor, Supervisor, Vendor
from server.utils.model_fields import random_slug

from .constants import (
    ACTIVITY_PAYLOADS,
    FEMALE_NAMES,
    LAST_NAMES,
    MALE_NAMES,
    ORGANIZATION_PAYLOAD,
    SCHOOL_PAYLOAD,
)


class Command(BaseCommand):
    help = "Creates test users for development"

    def add_arguments(self, parser):
        parser.add_argument(
            "--delete",
            action="store_true",
            help="delete all the test users",
        )

    def test_random_slug(self):
        return f"test_{random_slug()[5:]}"

    def create_admin(self, email):
        try:
            user = get_user_model().objects.create_superuser(
                self.test_random_slug(), email, "Aa123456789"
            )
            self.stdout.write(
                self.style.SUCCESS(f"Successfully created user with {user.email}")
            )
            return user
        except IntegrityError:
            self.stdout.write(
                self.style.WARNING("Dev admin already exists. Skipping...")
            )

    def create_user(self, user_model, email, password, name):
        try:
            user = user_model.objects.create(
                username=self.test_random_slug(),
                email=email,
                password=password,
                name=name,
            )
            user.set_password(user.password)
            user.save()
            self.stdout.write(
                self.style.SUCCESS(f"Successfully created user with {user.email}")
            )
            return user

        except IntegrityError:
            self.stdout.write(
                self.style.WARNING(f"{email} already exists. Skipping...")
            )

    def create_all(self, entitiesPrefix=""):
        self.create_admin(f"{entitiesPrefix}admin@example.com")

        consumers = []
        for i, name_record in enumerate(zip(MALE_NAMES, LAST_NAMES)):
            first_name, last_name = name_record
            user = self.create_user(
                Consumer,
                f"{entitiesPrefix}consumer-{i}@example.com",
                "Aa123456789",
                f"{first_name} {last_name}",
            )
            if user:
                user.profile.gender = user.profile.Gender.MALE
                user.profile.save()
                consumers.append(user)

        for i, name_record in enumerate(zip(FEMALE_NAMES, LAST_NAMES)):
            first_name, last_name = name_record
            user = self.create_user(
                Consumer,
                f"{entitiesPrefix}consumer-1{i}@example.com",
                "Aa123456789",
                f"{first_name} {last_name}",
            )
            if user:
                user.profile.gender = user.profile.Gender.FEMALE
                user.profile.save()
                consumers.append(user)

        if len(consumers):
            prev_email = consumers[0].email
            consumers[0].email = f"{entitiesPrefix}consumer@example.com"
            consumers[0].save()
            self.stdout.write(
                self.style.SUCCESS(
                    f"Successfully changed {prev_email} to {consumers[0].email}"
                )
            )

        coord = self.create_user(
            Coordinator,
            f"{entitiesPrefix}coord@example.com",
            "Aa123456789",
            "דוד כהן",
        )

        instructor = self.create_user(
            Instructor,
            f"{entitiesPrefix}instructor@example.com",
            "Aa123456789",
            "דן יוסופוב",
        )

        self.create_user(
            Supervisor,
            f"{entitiesPrefix}supervisor@example.com",
            "Aa123456789",
            "שמעון יצחק",
        )

        vendor = self.create_user(
            Vendor,
            f"{entitiesPrefix}vendor@example.com",
            "Aa123456789",
            "משי בר אל",
        )

        if not (len(consumers) and coord and instructor and vendor):
            return self.stdout.write(
                self.style.ERROR(
                    """Users creation failed - already exist.
                    use --delete option to delete the users and re-run"""
                )
            )

        org = Organization.objects.create(
            slug=self.test_random_slug(),
            **ORGANIZATION_PAYLOAD,
        )
        self.stdout.write(self.style.SUCCESS("Successfully created Organization"))

        school = School.objects.create(slug=self.test_random_slug(), **SCHOOL_PAYLOAD)
        self.stdout.write(self.style.SUCCESS("Successfully created School"))

        OrganizationMember.objects.bulk_create(
            [
                OrganizationMember(organization=org, user=instructor),
                OrganizationMember(organization=org, user=vendor),
            ]
        )
        self.stdout.write(
            self.style.SUCCESS("Successfully created OrganizationMember relations")
        )

        SchoolMember.objects.create(school=school, user=coord)
        SchoolMember.objects.bulk_create(
            [SchoolMember(school=school, user=consumer) for consumer in consumers]
        )
        self.stdout.write(
            self.style.SUCCESS("Successfully created SchoolMember relations")
        )

        activity_one, activity_two = Activity.objects.bulk_create(
            map(
                lambda activity: Activity(
                    slug=self.test_random_slug(),
                    originization=org,
                    **activity,
                ),
                ACTIVITY_PAYLOADS,
            )
        )
        self.stdout.write(self.style.SUCCESS("Successfully created Activities"))

        activity_order_one = SchoolActivityOrder.objects.create(
            slug=self.test_random_slug(),
            school=school,
            activity=activity_one,
            status=SchoolActivityOrder.Status.APPROVED,
        )
        SchoolActivityOrder.objects.create(
            slug=self.test_random_slug(),
            school=school,
            activity=activity_two,
            status=SchoolActivityOrder.Status.PENDING_ADMIN_APPROVAL,
        )
        self.stdout.write(self.style.SUCCESS("Successfully created ActivityOrders"))

        group_one = SchoolActivityGroup.objects.create(
            slug=self.test_random_slug(),
            activity_order=activity_order_one,
            name="Group One",
            description="Group One Description",
            instructor=instructor,
        )
        group_two = SchoolActivityGroup.objects.create(
            slug=self.test_random_slug(),
            activity_order=activity_order_one,
            name="Container Only",
            description="Container Only",
            group_type=SchoolActivityGroup.GroupTypes.CONTAINER_ONLY,
        )
        SchoolActivityGroup.objects.create(
            slug=self.test_random_slug(),
            activity_order=activity_order_one,
            name="Cancelled Group",
            description="Cancelled Group",
            group_type=SchoolActivityGroup.GroupTypes.DISABLED_CONSUMERS,
        )

        group_one.consumers.add(consumers[0])
        group_two.consumers.add(consumers[1])
        self.stdout.write(
            self.style.SUCCESS("Successfully created SchoolActivityGroups")
        )

        today = datetime.now(tz=timezone.utc).replace(microsecond=0, second=0, minute=0)
        event_orders = []
        events = []
        for i in range(-10, 20):
            event_data = {
                "school_group": group_one,
                "locations_name": "חדר 202",
                "start_time": today + timedelta(days=i * 7),
                "end_time": today + timedelta(days=i * 7) + timedelta(hours=1.5),
            }

            event_orders.append(
                EventOrder(
                    slug=self.test_random_slug(),
                    status=EventOrder.Status.PENDING_APPROVAL,
                    **event_data,
                )
            )

            event_orders.append(
                EventOrder(
                    slug=self.test_random_slug(),
                    status=EventOrder.Status.APPROVED,
                    **event_data,
                )
            )
            events.append(
                Event(
                    slug=self.test_random_slug(),
                    event_order=event_orders[-1],
                    **event_data,
                )
            )

        Event.objects.bulk_create(events)
        self.stdout.write(self.style.SUCCESS("Successfully created EventOrders"))
        EventOrder.objects.bulk_create(event_orders)
        self.stdout.write(self.style.SUCCESS("Successfully created Events"))

    def delete_model_test_entities(self, model):
        items = model.objects.filter(slug__startswith="test_")
        count = items.count()
        items.delete()
        self.stdout.write(
            self.style.SUCCESS(f"{count} {model.__name__} items deleted successfully")
        )

    def delete_all(self):
        users = get_user_model().objects.filter(username__startswith="test_")
        total_users = users.count()
        users.delete()
        self.stdout.write(
            self.style.SUCCESS(f"{total_users} users deleted successfully")
        )

        self.delete_model_test_entities(Event)
        self.delete_model_test_entities(EventOrder)
        self.delete_model_test_entities(SchoolActivityGroup)
        self.delete_model_test_entities(SchoolActivityOrder)
        self.delete_model_test_entities(Activity)
        self.delete_model_test_entities(School)
        self.delete_model_test_entities(Organization)

    def handle(self, *args, **options):
        if options["delete"]:
            return self.delete_all()

        self.create_all()
        self.create_all(entitiesPrefix="test-")
