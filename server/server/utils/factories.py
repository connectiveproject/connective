from importlib import import_module

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from server.users.forms import ConnectiveFormFactory


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
