from django.db.models import (
    Model,
    ForeignKey,
    CharField,
    SET_NULL,
    ManyToManyField,
)

from server.events.models import Event
from server.schools.models import random_slug
from server.users.models import User


class Image(Model):
    slug = CharField(
        max_length=40,
        default=random_slug,
        unique=True,
    )
    image_b64 = CharField()


class Post(Model):
    slug = CharField(
        max_length=40,
        default=random_slug,
        unique=True,
    )
    event = ForeignKey(
        to=Event,
        on_delete=SET_NULL,
        null=True,
    )
    author = ForeignKey(
        to=User,
        on_delete=SET_NULL,
        null=True,
    )
    post_content = CharField()
    images = ManyToManyField(
        to=Image,
    )
