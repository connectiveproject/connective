from django.contrib.auth import get_user_model
from django.db import models

from server.utils.db_utils import get_base_model
from server.utils.model_fields import random_slug


class TermsOfUseDocumentManager(models.Manager):
    def sign(self, user):
        return TermsOfUseSignature.objects.create(user=user, document=super().last())


class TermsOfUseDocument(get_base_model()):

    objects = TermsOfUseDocumentManager()

    slug = models.CharField(max_length=40, default=random_slug, unique=True)
    document_name = models.CharField(blank=True, max_length=50)
    document_text = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)


class TermsOfUseSignature(get_base_model()):
    document = models.ForeignKey(
        TermsOfUseDocument,
        on_delete=models.SET_NULL,
        null=True,
        related_name="signatures",
    )
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="signatures",
    )
    created = models.DateTimeField(auto_now_add=True)
