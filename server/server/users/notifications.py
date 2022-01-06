from __future__ import annotations

from typing import Dict, Tuple


def registry_entry(title_label: str, action_label: str, link: str) -> Dict[str]:
    return locals()


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

    def create(registry: Tuple) -> NotificationRegistry:
        res: NotificationRegistry = NotificationRegistry(registry)
        return res
