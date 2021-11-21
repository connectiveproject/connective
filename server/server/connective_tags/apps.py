from django.apps import AppConfig


class ConnectiveTagsConfig(AppConfig):
    name = "server.connective_tags"

    def ready(self):
        try:
            import server.connective_tags.signals  # noqa F401
        except ImportError:
            pass
