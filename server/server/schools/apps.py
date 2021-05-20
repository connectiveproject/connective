from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class SchoolsConfig(AppConfig):
    name = "server.schools"
    verbose_name = _("Schools")

    def ready(self):
        try:
            import server.schools.signals  # noqa F401
        except ImportError:
            pass
