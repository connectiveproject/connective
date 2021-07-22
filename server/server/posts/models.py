from django.db.models import (
    SET_NULL,
    CharField,
    DateTimeField,
    ForeignKey,
    ImageField,
    Model,
    TextField,
)

from server.events.models import Event
from server.users.models import User
from server.utils.model_fields import random_slug


class Post(Model):
    slug = CharField(
        max_length=40,
        default=random_slug,
        unique=True,
    )
    creation_time = DateTimeField(
        auto_now=True,
        null=False,
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
    # images_b64 = ArrayField(
    #     TextField(),
    #     null=True,
    # )
    images_b64 = ImageField(
        null=True,
        blank=True,
    )
