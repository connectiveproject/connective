from django.contrib.auth import get_user_model
from django.db import models

from server.events.models import Event
from server.utils.model_fields import random_slug


class Post(models.Model):
    slug = models.CharField(
        max_length=40,
        default=random_slug,
        unique=True,
    )
    creation_time = models.DateTimeField(
        auto_now_add=True,
    )
    event = models.ForeignKey(
        Event,
        on_delete=models.SET_NULL,
        blank=False,
        null=True,
    )
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        blank=False,
        null=True,
    )
    post_content = models.TextField()


class PostImage(models.Model):
    slug = models.CharField(max_length=40, default=random_slug, unique=True)
    image_url = models.ImageField()
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="images",
    )

    def __str__(self):
        return f"{self.image_url} | {self.slug} | {self.post.slug}"
