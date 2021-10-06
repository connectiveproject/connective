import analytics


def identify_track(user, event_name, properties=None):
    analytics.identify(
        user.slug,
        {
            "name": user.name,
            "email": user.email,
            "user_type": user.user_type,
        },
    )
    return analytics.track(user.slug, event_name, properties)
