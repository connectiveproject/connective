PRIV_CALENDAR_VIEW = "PRIV_CALENDAR_VIEW"
PRIV_CALENDAR_EDIT = "PRIV_CALENDAR_EDIT"
PRIV_CONTENT_EDIT = "PRIV_CONTENT_EDIT"
PRIV_CONTENT_VIEW = "PRIV_CONTENT_VIEW"
PRIV_ACTIVITIES_VIEW = "PRIV_ACTIVITIES_VIEW"
PRIV_ACTIVITIES_EDIT = "PRIV_ACTIVITIES_EDIT"


ROLES = {
    "VENDOR_ADMIN": frozenset(
        [
            PRIV_CALENDAR_VIEW,
            PRIV_CALENDAR_EDIT,
            PRIV_ACTIVITIES_VIEW,
            PRIV_ACTIVITIES_EDIT,
        ]
    ),
    "COORDINATOR_ADMIN": frozenset(PRIV_ACTIVITIES_VIEW),
    "CONTENT_EDITOR": frozenset([PRIV_CONTENT_EDIT, PRIV_CONTENT_VIEW]),
    "INSTRUCTOR": frozenset([PRIV_CONTENT_VIEW]),
    "CUSTOMER_ADMIN": frozenset(
        [PRIV_CALENDAR_VIEW, PRIV_CALENDAR_EDIT, PRIV_CONTENT_EDIT, PRIV_CONTENT_VIEW]
    ),
}