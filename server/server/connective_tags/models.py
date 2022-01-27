from django.db import models
from django.utils.translation import gettext_lazy as _
from taggit.models import GenericTaggedItemBase, TagBase

from server.utils.db_utils import get_base_model


class ConnectiveTag(TagBase, get_base_model()):
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
