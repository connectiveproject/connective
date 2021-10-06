import logging

import analytics
from django.core import exceptions

from server.utils.logging.constants import SCHOOL_MEMBER

logger = logging.getLogger(__name__)

EVENT_SESSION_LOGIN = "session_login"
EVENT_APP_LOGIN = "app_login"
EVENT_INITIAL_PASSWORD_CREATED = "initial_password_created"


def identify_track(user, event_name, properties=None):
    traits = (
        {
            "name": user.name,
            "email": user.email,
            "user_type": user.user_type,
        },
    )
    if user.user_type in [user.Types.CONSUMER, user.Types.CONSUMER]:
        try:
            traits["school"] = user.school_member.school.name
        except exceptions.ObjectDoesNotExist:
            logger.exception(
                f"{SCHOOL_MEMBER} user pk: {user.pk} email: {user.email} has no school_member or school"
            )

    analytics.identify(
        user.slug,
        traits,
    )

    return analytics.track(user.slug, event_name, properties)
