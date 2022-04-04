PRIV_CALENDAR_VIEW = "PRIV_CALENDAR_VIEW"
PRIV_CALENDAR_EDIT = "PRIV_CALENDAR_EDIT"
PRIV_CONTENT_EDIT = "PRIV_CONTENT_EDIT"
PRIV_CONTENT_VIEW = "PRIV_CONTENT_VIEW"
PRIV_ACTIVITIES_VIEW = "PRIV_ACTIVITIES_VIEW"
PRIV_ACTIVITIES_EDIT = "PRIV_ACTIVITIES_EDIT"
PRIV_USER_CONSUMER_EDIT = "PRIV_USER_CONSUMER_EDIT"
PRIV_USER_CONSUMER_VIEW = "PRIV_USER_CONSUMER_VIEW"
PRIV_USER_COORDINATOR_EDIT = "PRIV_USER_COORDINATOR_EDIT"
PRIV_USER_INSTRUCTOR_EDIT = "PRIV_USER_INSTRUCTOR_EDIT"
PRIV_USER_INSTRUCTOR_VIEW = "PRIV_USER_INSTRUCTOR_VIEW"
PRIV_USER_INSTRUCTOR_VIEW_ALL = "PRIV_USER_INSTRUCTOR_VIEW_ALL"
PRIV_EVENT_ORDER_VIEW = "PRIV_EVENT_ORDER_VIEW"
PRIV_EVENT_ORDER_EDIT = "PRIV_EVENT_ORDER_EDIT"
PRIV_EVENT_ORDER_APPROVE = "PRIV_EVENT_ORDER_APPROVE"
PRIV_EVENT_VIEW = "PRIV_EVENT_VIEW"
PRIV_EVENT_EDIT = "PRIV_EVENT_EDIT"
PRIV_EVENT_EDIT_MY_ONLY = "PRIV_EVENT_EDIT_MY_ONLY"


ROLE_VENDOR_ADMIN = "VENDOR_ADMIN"
ROLE_COORDINATOR_ADMIN = "COORDINATOR_ADMIN"
ROLE_CONTENT_EDITOR = "CONTENT_EDITOR"
ROLE_INSTRUCTOR = "INSTRUCTOR"
ROLE_CUSTOMER_ADMIN = "CUSTOMER_ADMIN"

ROLES = {
    ROLE_VENDOR_ADMIN: frozenset(
        [
            PRIV_CALENDAR_VIEW,
            PRIV_CALENDAR_EDIT,
            PRIV_ACTIVITIES_VIEW,
            PRIV_ACTIVITIES_EDIT,
            PRIV_USER_INSTRUCTOR_EDIT,
            PRIV_USER_INSTRUCTOR_VIEW,
            PRIV_EVENT_ORDER_VIEW,
            PRIV_EVENT_ORDER_EDIT,
            PRIV_EVENT_ORDER_APPROVE,
            PRIV_EVENT_VIEW,
            PRIV_EVENT_EDIT,
            PRIV_EVENT_EDIT_MY_ONLY,
        ]
    ),
    ROLE_COORDINATOR_ADMIN: frozenset(
        [
            PRIV_ACTIVITIES_VIEW,
            PRIV_USER_CONSUMER_EDIT,
            PRIV_USER_CONSUMER_VIEW,
            PRIV_USER_COORDINATOR_EDIT,
            PRIV_USER_INSTRUCTOR_VIEW,
            PRIV_USER_INSTRUCTOR_VIEW_ALL,
            PRIV_EVENT_ORDER_VIEW,
            PRIV_EVENT_ORDER_EDIT,
            PRIV_EVENT_VIEW,
            PRIV_EVENT_EDIT,
            PRIV_EVENT_EDIT_MY_ONLY,
        ]
    ),
    ROLE_CONTENT_EDITOR: frozenset([PRIV_CONTENT_EDIT, PRIV_CONTENT_VIEW]),
    ROLE_INSTRUCTOR: frozenset(
        [
            PRIV_CONTENT_VIEW,
            PRIV_USER_CONSUMER_VIEW,
            PRIV_USER_INSTRUCTOR_VIEW,
            PRIV_EVENT_VIEW,
            PRIV_EVENT_EDIT_MY_ONLY,
        ]
    ),
    ROLE_CUSTOMER_ADMIN: frozenset(
        [
            PRIV_CALENDAR_VIEW,
            PRIV_CALENDAR_EDIT,
            PRIV_CONTENT_EDIT,
            PRIV_CONTENT_VIEW,
            PRIV_USER_CONSUMER_EDIT,
            PRIV_USER_CONSUMER_VIEW,
            PRIV_USER_COORDINATOR_EDIT,
            PRIV_USER_INSTRUCTOR_EDIT,
            PRIV_USER_INSTRUCTOR_VIEW,
            PRIV_USER_INSTRUCTOR_VIEW_ALL,
            PRIV_EVENT_ORDER_VIEW,
            PRIV_EVENT_ORDER_EDIT,
            PRIV_EVENT_ORDER_APPROVE,
            PRIV_EVENT_VIEW,
            PRIV_EVENT_EDIT,
            PRIV_EVENT_EDIT_MY_ONLY,
        ]
    ),
}
