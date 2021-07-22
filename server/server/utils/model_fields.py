import random
import uuid

from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class PhoneNumberField(models.CharField):
    def __init__(self, verbose_name=None, name=None, **kwargs):
        kwargs.setdefault("max_length", 15)
        super().__init__(verbose_name, name, **kwargs)

    default_validators = [
        RegexValidator(
            regex=r"^\d{9,15}$",
            message=_("Phone number must be between 9-15 digits."),
        )
    ]
    description = _("Phone Number")


class IdNumberField(models.CharField):
    def __init__(self, verbose_name=None, name=None, **kwargs):
        kwargs.setdefault("max_length", 9)
        super().__init__(verbose_name, name, **kwargs)

    default_validators = [
        RegexValidator(
            regex=r"^\d{9}$",
            message=_("Id number must be between 9 digits."),
        )
    ]
    description = _("Id number")


def random_slug():
    return uuid.uuid4().hex.upper()[0 : random.randint(10, 22)]  # noqa
