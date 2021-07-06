from datetime import datetime, timedelta

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import IntegrityError
from django.utils import timezone

from server.events.models import Event
from server.organizations.models import (
    Activity,
    Organization,
    OrganizationMember,
    SchoolActivityGroup,
    SchoolActivityOrder,
)
from server.schools.models import School, SchoolMember
from server.users.models import Consumer, Coordinator, Instructor, Vendor

from .constants import (
    activity_payloads,
    female_names,
    last_names,
    male_names,
    organization_payload,
    school_payload,
)


class Command(BaseCommand):
    help = "Creates test users for development"

    def add_arguments(self, parser):
        "parser.add_argument('some_number', nargs='+', type=int)"
        pass

    def create_admin(self):
        try:
            user = get_user_model().objects.create_superuser(
                "admin", "admin@example.com", "Aa123456789"
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
            user = user_model.objects.create(email=email, password=password, name=name)
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

    def create_all(self):
        self.create_admin()

        consumers = []
        for i, name_record in enumerate(zip(male_names, last_names)):
            first_name, last_name = name_record
            user = self.create_user(
                Consumer,
                f"consumer-{i}@example.com",
                "Aa123456789",
                f"{first_name} {last_name}",
            )
            if user:
                user.profile.gender = user.profile.Gender.MALE
                user.profile.save()
                consumers.append(user)

        for i, name_record in enumerate(zip(female_names, last_names)):
            first_name, last_name = name_record
            user = self.create_user(
                Consumer,
                f"consumer-1{i}@example.com",
                "Aa123456789",
                f"{first_name} {last_name}",
            )
            if user:
                user.profile.gender = user.profile.Gender.FEMALE
                user.profile.save()
                consumers.append(user)

        if len(consumers):
            prev_email = consumers[0].email
            consumers[0].email = "consumer@example.com"
            consumers[0].save()
            self.stdout.write(
                self.style.SUCCESS(
                    f"Successfully changed {prev_email} to {consumers[0].email}"
                )
            )

        coord = self.create_user(
            Coordinator,
            "coord@example.com",
            "Aa123456789",
            "דוד כהן",
        )

        instructor = self.create_user(
            Instructor,
            "instructor@example.com",
            "Aa123456789",
            "דן יוסופוב",
        )
        vendor = self.create_user(
            Vendor,
            "vendor@example.com",
            "Aa123456789",
            "משי בר אל",
        )

        if not (len(consumers) and coord and instructor and vendor):
            return self.stdout.write(
                self.style.ERROR(
                    "Users creation failed - already exist.\n\
You may flush all db using: `python manage.py flush`\n\
USE WITH CAUTION - THIS DELETES EVERYTHING"
                )
            )

        org = Organization.objects.create(**organization_payload)
        self.stdout.write(self.style.SUCCESS("Successfully created Organization"))

        school = School.objects.create(**school_payload)
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
                lambda activity: Activity(**activity, originization=org),
                activity_payloads,
            )
        )
        self.stdout.write(self.style.SUCCESS("Successfully created Activities"))

        activity_order_one = SchoolActivityOrder.objects.create(
            school=school,
            activity=activity_one,
            status=SchoolActivityOrder.Status.APPROVED,
        )
        SchoolActivityOrder.objects.create(
            school=school,
            activity=activity_two,
            status=SchoolActivityOrder.Status.PENDING_ADMIN_APPROVAL,
        )
        self.stdout.write(self.style.SUCCESS("Successfully created ActivityOrders"))

        group_one = SchoolActivityGroup.objects.create(
            activity_order=activity_order_one,
            name="Group One",
            description="Group One Description",
            instructor=instructor,
        )
        group_two = SchoolActivityGroup.objects.create(
            activity_order=activity_order_one,
            name="Container Only",
            description="Container Only",
            group_type=SchoolActivityGroup.GroupTypes.CONTAINER_ONLY,
        )
        SchoolActivityGroup.objects.create(
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
        events = []
        for i in range(20):
            events.append(
                Event(
                    school_group=group_one,
                    locations_name="חדר 202",
                    start_time=today + timedelta(days=i * 7),
                    end_time=today + timedelta(days=i * 7) + timedelta(hours=1.5),
                )
            )

        Event.objects.bulk_create(events)
        self.stdout.write(self.style.SUCCESS("Successfully created Events"))

    def handle(self, *args, **options):
        self.create_all()
