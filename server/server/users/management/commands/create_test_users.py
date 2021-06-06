from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import IntegrityError

from server.users.models import Consumer, Coordinator, Vendor


class Command(BaseCommand):
    help = "Creates test users for development"

    def add_arguments(self, parser):
        "parser.add_argument('some_number', nargs='+', type=int)"
        pass

    def createUser(self, userModel, email, password):
        try:
            user = userModel.objects.create(email=email, password=password)
            user.set_password(user.password)
            user.save()

            self.stdout.write(
                self.style.SUCCESS(f"Successfully created user with {user.email}")
            )
        except IntegrityError:
            self.stdout.write(
                self.style.WARNING(f"{email} already exists. Skipping...")
            )

    def createAdmin(self):
        try:
            user = get_user_model().objects.create_superuser(
                "admin", "admin@example.com", "Aa123456789"
            )
            self.stdout.write(
                self.style.SUCCESS(f"Successfully created user with {user.email}")
            )
        except IntegrityError:
            self.stdout.write(
                self.style.WARNING("Dev admin already exists. Skipping...")
            )

    def handle(self, *args, **options):
        if not settings.DEBUG:
            raise RuntimeError("create_test_users is meant for dev environments.")

        self.createUser(Coordinator, "coord@example.com", "Aa123456789")
        self.createUser(Consumer, "consumer@example.com", "Aa123456789")
        self.createUser(Vendor, "vendor@example.com", "Aa123456789")
        self.createAdmin()