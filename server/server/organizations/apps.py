from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class OrganizationsConfig(AppConfig):
    name = "server.organizations"
    verbose_name = _("Organizations")

    def ready(self):
        try:
            import server.organizations.signals  # noqa F401
        except ImportError:
            pass
