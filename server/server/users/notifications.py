from __future__ import annotations

from importlib import import_module
from typing import Dict, Tuple

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


class NotificationRegistry:

    RETENTION_DAYS: int = 30

    EVENT_SCHEDULE_APPROVED = (
        "EVENT_SCHEDULE_APPROVED",
        "notifications.scheduleEventDeclined",
        "general.go",
        "/coor/event/{abc}",
        {},
    )

    EVENT_SCHEDULE_DECLINED = (
        "EVENT_SCHEDULE_DECLINED",
        "notifications.scheduleEventApproved",
        "general.go",
        "/coor/event/{abc}",
        {},
    )

    NEW_EVENT_REQUEST = (
        "NEW_EVENT_REQUEST",
        "notifications.newEventRequest",
        "general.go",
        "/vendor/event-request/{abc}",
        {},
    )

    def __init__(self, registry: Tuple):
        self.code = registry[0]
        self.title_label = registry[1]
        self.action_label = registry[2]
        self.link = registry[3]
        self.link_parameters = registry[4]

    def get_code(self) -> str:
        return self.code

    def get_title_label(self) -> str:
        return self.title_label

    def get_action_label(self) -> str:
        return self.action_label

    def get_link(self) -> str:
        return self.link

    def get_link_parameters(self) -> Dict[str, str]:
        return self.link_parameters

    def create(registry_code: str) -> NotificationRegistry:
        reg_list = get_notification_registry_list()
        result: NotificationRegistry = reg_list[registry_code]
        if not result:
            raise Exception(f"No such registry {registry_code}")
        return result


def add_registry_entry(
    registry_list: Dict[str, NotificationRegistry], registry_entry: Tuple
):
    registry_list[registry_entry[0]] = NotificationRegistry(registry_entry)


def init_registry() -> Dict[str, NotificationRegistry]:
    result: Dict[str, NotificationRegistry] = {}
    add_registry_entry(result, NotificationRegistry.EVENT_SCHEDULE_APPROVED)
    add_registry_entry(result, NotificationRegistry.EVENT_SCHEDULE_DECLINED)
    add_registry_entry(result, NotificationRegistry.NEW_EVENT_REQUEST)
    return result


registry_list: Dict[str, NotificationRegistry] = init_registry()


def get_notification_registry_list():
    try:
        return getattr(
            import_module(settings.NOTIFICATION_LIST.rsplit(".", 1)[0]),
            settings.NOTIFICATION_LIST.rsplit(".", 1)[1],
        )
    except ValueError:
        return registry_list
    except AttributeError:
        return registry_list
    except LookupError:
        raise ImproperlyConfigured(
            f"'{settings.NOTIFICATION_LIST}' has not been installed"
        )
