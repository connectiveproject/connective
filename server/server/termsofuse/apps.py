from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class TermsofuseConfig(AppConfig):
    name = "server.termsofuse"
    verbose_name = _("Terms Of Use")

    def ready(self):
        try:
            import server.termsofuse.signals  # noqa F401
        except ImportError:
            pass
