from __future__ import annotations

from collections import namedtuple
from importlib import import_module
from typing import Dict

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

NOTIFICATIONS_RETENTION_DAYS: int = 30

NotificationRegistry = namedtuple(
    "NotificationRegistry",
    ["code", "title_label", "action_label", "link", "link_parameters"],
)

EVENT_SCHEDULE_APPROVED = NotificationRegistry(
    "EVENT_SCHEDULE_APPROVED",
    "notifications.scheduleEventDeclined",
    "general.go",
    "/coor/event/{abc}",
    {},
)

EVENT_SCHEDULE_APPROVED = NotificationRegistry(
    "EVENT_SCHEDULE_APPROVED",
    "notifications.scheduleEventDeclined",
    "general.go",
    "/coor/event/{abc}",
    {},
)

EVENT_SCHEDULE_DECLINED = NotificationRegistry(
    "EVENT_SCHEDULE_DECLINED",
    "notifications.scheduleEventApproved",
    "general.go",
    "/coor/event/{abc}",
    {},
)

NEW_EVENT_REQUEST = NotificationRegistry(
    "NEW_EVENT_REQUEST",
    "notifications.newEventRequest",
    "general.go",
    "/vendor/event-request/{abc}",
    {},
)


def get_notification_registry(registry_code: str) -> NotificationRegistry:
    reg_list = get_notification_registry_list()
    result: NotificationRegistry = reg_list[registry_code]
    if not result:
        raise Exception(f"No such registry {registry_code}")
    return result


def add_registry_entry(
    registry_list: Dict[str, NotificationRegistry], registry_entry: NotificationRegistry
):
    registry_list[registry_entry.code] = registry_entry


def init_registry() -> Dict[str, NotificationRegistry]:
    result: Dict[str, NotificationRegistry] = {}
    add_registry_entry(result, EVENT_SCHEDULE_APPROVED)
    add_registry_entry(result, EVENT_SCHEDULE_DECLINED)
    add_registry_entry(result, NEW_EVENT_REQUEST)
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
