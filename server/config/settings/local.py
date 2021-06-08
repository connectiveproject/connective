import os

from .base import *  # noqa
from .base import env

# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = True
# https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = env(
    "DJANGO_SECRET_KEY",
    default="8KRy3qHYEiiz1VzdpG58RegxiBcjdp9yAFnmf56xAZn4hHIW7ZWRGAZKwuub3Msx",
)
# https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
GITPOD_WORKSPACE_URL = os.environ.get("GITPOD_WORKSPACE_URL")
GITPOD_WORKSPACE_ID = env(
    "GITPOD_WORKSPACE_ID", default=os.environ.get("GITPOD_WORKSPACE_ID")
)

ALLOWED_HOSTS = ["localhost", "0.0.0.0", "127.0.0.1", GITPOD_WORKSPACE_URL]

# CACHES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#caches
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "",
    }
}

# EMAIL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#email-host
EMAIL_HOST = "localhost"
# https://docs.djangoproject.com/en/dev/ref/settings/#email-port
EMAIL_PORT = 1025

# WhiteNoise
# ------------------------------------------------------------------------------
# http://whitenoise.evans.io/en/latest/django.html#using-whitenoise-in-development
INSTALLED_APPS = ["whitenoise.runserver_nostatic"] + INSTALLED_APPS  # noqa F405


# django-debug-toolbar
# ------------------------------------------------------------------------------
# https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#prerequisites
INSTALLED_APPS += ["debug_toolbar"]  # noqa F405
# https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#middleware
MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]  # noqa F405
# https://django-debug-toolbar.readthedocs.io/en/latest/configuration.html#debug-toolbar-config
DEBUG_TOOLBAR_CONFIG = {
    "DISABLE_PANELS": ["debug_toolbar.panels.redirects.RedirectsPanel"],
    "SHOW_TEMPLATE_CONTEXT": True,
}
# https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#internal-ips
INTERNAL_IPS = ["127.0.0.1", "10.0.2.2"]


# django-extensions
# ------------------------------------------------------------------------------
# https://django-extensions.readthedocs.io/en/latest/installation_instructions.html#configuration
INSTALLED_APPS += ["django_extensions"]  # noqa F405
# Celery
# ------------------------------------------------------------------------------
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#task-always-eager
CELERY_TASK_ALWAYS_EAGER = True
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#task-eager-propagates
CELERY_TASK_EAGER_PROPAGATES = True
# Your stuff...
# ------------------------------------------------------------------------------
if GITPOD_WORKSPACE_URL:
    DATABASES = {
        "default": env.db(
            "postgresql://gitpod@localhost/server",
            default="postgres:///server",
        ),
    }
    DATABASES["default"]["ATOMIC_REQUESTS"] = True
    CORS_ORIGIN_ALLOW_ALL = True

else:
    CORS_ALLOWED_ORIGINS = [
        "http://localhost:8080",
        "http://127.0.0.1:8080",
    ]

if GITPOD_WORKSPACE_ID:
    RESET_BASE_URL = f"https://8000-{GITPOD_WORKSPACE_URL[8:]}"
