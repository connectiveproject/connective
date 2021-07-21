from django.contrib.postgres.fields import ArrayField
from django.db.models import SET_NULL, CharField, ForeignKey, Model, TextField

from server.events.models import Event
from server.users.models import User
from server.utils.model_fields import random_slug


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
    images_b64 = ArrayField(
        TextField(),
        null=True,
    )
