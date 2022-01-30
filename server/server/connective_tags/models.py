from django.db import models
from django.utils.translation import gettext_lazy as _
from taggit.models import GenericTaggedItemBase, TagBase

from server.utils.db_utils import get_base_model


class ConnectiveTag(TagBase, get_base_model()):

    # slug should be equals to name. We need to allow non-Engilsh keys,
    # therefore we override the slug field to allow all characters. TODO: We might
    # need to limit it to avoid whitespace or other characters
    slug = models.CharField(max_length=40, unique=True, blank=False, null=False)

    category = models.CharField(
        max_length=30, null=False, blank=False, default="general"
    )

    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")


class ConnectiveTaggedItem(GenericTaggedItemBase, get_base_model()):

    # Here is where you provide your custom Tag class.
    tag = models.ForeignKey(
        ConnectiveTag,
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_items",
    )
