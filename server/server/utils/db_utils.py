from importlib import import_module

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ImproperlyConfigured
from django.db import models
from rest_framework.permissions import BasePermission


def get_base_model():
    """
    Return the base model that is active in this project.
    """
    try:
        return import_module(settings.BASE_MODEL).BaseModel
    except ValueError:
        return models.Model
    except AttributeError:
        return models.Model
    except LookupError:
        raise ImproperlyConfigured(
            f"BASE_MODEL refers to model '{settings.BASE_MODEL}' that has not been installed"
        )


def get_additional_permissions_write():
    try:
        return getattr(
            import_module(settings.ADDITIONAL_PERMISSIONS_WRITE.rsplit(".", 1)[0]),
            settings.ADDITIONAL_PERMISSIONS_WRITE.rsplit(".", 1)[1],
        )
    except ValueError:
        return NoPermission
    except AttributeError:
        return NoPermission
    except LookupError:
        return NoPermission


def get_additional_permissions_readonly():
    try:
        return getattr(
            import_module(settings.ADDITIONAL_PERMISSIONS_READONLY.rsplit(".", 1)[0]),
            settings.ADDITIONAL_PERMISSIONS_READONLY.rsplit(".", 1)[1],
        )
    except ValueError:
        return NoPermission
    except AttributeError:
        return NoPermission
    except LookupError:
        return NoPermission


class NoPermission(BasePermission):
    def has_permission(self, request, view):
        return False


def get_base_abstract_user_model():
    """
    Return the base mixin that is active in this project.
    """
    try:
        return import_module(settings.BASE_MODEL).BaseAbstractUser
    except ValueError:
        return AbstractUser
    except AttributeError:
        return AbstractUser
    except LookupError:
        raise ImproperlyConfigured(
            f"BASE_MIXIN refers to model '{settings.BASE_MIXIN}' that has not been installed"
        )
