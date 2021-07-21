from django.db.models import (
    Model,
    ForeignKey,
    CharField,
    SET_NULL,
    ManyToManyField,
    TextField
)

from server.users.models import User
from server.events.models import Event
from server.utils.model_fields import random_slug


class Image(Model):
    slug = CharField(
        max_length=40,
        default=random_slug,
        unique=True,
    )
    image_b64 = TextField()


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
    post_content = TextField()
    images = ManyToManyField(
        to=Image,
    )
