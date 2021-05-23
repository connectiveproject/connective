from django.contrib.auth.models import AbstractUser
from django.db.models import CharField, Manager, TextChoices
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """Default user for server."""

    class Types(TextChoices):
        CONSUMER = "CONSUMER", "Consumer"
        COORDINATOR = "COORDINATOR", "Coordinator"
        VENDOR = "VENDOR", "Vendor"

    base_user_type = Types.CONSUMER

    user_type = CharField(
        _("Type"), max_length=50, choices=Types.choices, default=base_user_type
    )

    #: First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore
    last_name = None  # type: ignore

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})

    def save(self, *args, **kwargs):
        if not self.id:
            self.user_type = self.base_user_type
        return super().save(*args, **kwargs)


class ConsumerManager(Manager):
    def get_queryset(self, *args, **kwargs):
        return (
            super()
            .get_queryset(*args, **kwargs)
            .filter(
                user_type=User.Types.CONSUMER,
            )
        )


class CoordinatorManager(Manager):
    def get_queryset(self, *args, **kwargs):
        return (
            super()
            .get_queryset(*args, **kwargs)
            .filter(
                user_type=User.Types.COORDINATOR,
            )
        )


class VendorManager(Manager):
    def get_queryset(self, *args, **kwargs):
        return (
            super()
            .get_queryset(*args, **kwargs)
            .filter(
                user_type=User.Types.VENDOR,
            )
        )


class Consumer(User):
    base_user_type = User.Types.CONSUMER
    objects = ConsumerManager()

    class Meta:
        proxy = True


class Coordinator(User):
    base_user_type = User.Types.COORDINATOR
    objects = CoordinatorManager()

    class Meta:
        proxy = True


class Vendor(User):
    base_user_type = User.Types.VENDOR
    objects = VendorManager()

    class Meta:
        proxy = True
