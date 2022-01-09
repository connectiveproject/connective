from __future__ import annotations

from typing import Dict, Tuple


class NotificationRegistry:

    RETENTION_DAYS: int = 30

    EVENT_SCHEDULE_APPROVED = (
        "EVENT_SCHEDULE_APPROVED",
        "notifications.scheduleEventDeclined",
        "general.go",
        "/coor/event/{abc}",
    )

    EVENT_SCHEDULE_DECLINED = (
        "EVENT_SCHEDULE_DECLINED",
        "notifications.scheduleEventApproved",
        "general.go",
        "/coor/event/{abc}",
    )

    NEW_EVENT_REQUEST = (
        "NEW_EVENT_REQUEST",
        "notifications.newEventRequest",
        "general.go",
        "/vendor/event-request/{abc}",
    )

    NEW_EVENT_SUMMARY_SUBMITTED = (
        "NEW_EVENT_SUMMARY_SUBMITTED",
        "notifications.newEventSummarySubmitted",
        "general.go",
        "GatekeeperEvents",
    )

    def __init__(self, registry: Tuple):
        self.code = registry[0]
        self.title_label = registry[1]
        self.action_label = registry[2]
        self.link = registry[3]

    def get_code(self):
        return self.code

    def get_title_label(self):
        return self.title_label

    def get_action_label(self):
        return self.action_label

    def get_link(self):
        return self.link

    def create(registry_code: str) -> NotificationRegistry:
        result: NotificationRegistry = registry_list[registry_code]
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
    add_registry_entry(result, NotificationRegistry.NEW_EVENT_SUMMARY_SUBMITTED)
    return result


registry_list: Dict[str, NotificationRegistry] = init_registry()
