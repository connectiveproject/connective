from importlib import import_module

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from server.users.forms import ConnectiveFormFactory
from server.users.models import UserUtil


def get_form_factory() -> ConnectiveFormFactory:
    try:
        return getattr(
            import_module(settings.FORM_FACTORY.rsplit(".", 1)[0]),
            settings.FORM_FACTORY.rsplit(".", 1)[1],
        )
    except ValueError:
        return ConnectiveFormFactory
    except AttributeError:
        return ConnectiveFormFactory
    except LookupError:
        raise ImproperlyConfigured(
            f"BASE_MIXIN refers to model '{settings.FORM_FACTORY}' that has not been installed"
        )


def get_user_utils() -> UserUtil:
    try:
        return getattr(
            import_module(settings.USER_UTIL.rsplit(".", 1)[0]),
            settings.USER_UTIL.rsplit(".", 1)[1],
        )()
    except ValueError:
        return UserUtil()
    except AttributeError:
        return UserUtil()
    except LookupError:
        raise ImproperlyConfigured(
            f"BASE_MIXIN refers to model '{settings.USER_UTIL}' that has not been installed"
        )
