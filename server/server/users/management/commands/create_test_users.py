from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError


class Command(BaseCommand):
    help = "Creates test users for development"

    def add_arguments(self, parser):
        "parser.add_argument('some_number', nargs='+', type=int)"
        pass

    def handle(self, *args, **options):
        if not settings.DEBUG:
            raise RuntimeError("create_test_users is meant for dev environments.")
        try:
            user = get_user_model().objects.create_superuser(
                "admin", "admin@example.com", "Aa123456789"
            )
            self.stdout.write(
                self.style.SUCCESS(f"Successfully created user with {user.email}")
            )
        except IntegrityError:
            raise CommandError("Dev admin already exists")
