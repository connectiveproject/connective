from django.db import models

from server.utils.model_fields import random_slug


class TermsOfUseDocument(models.Model):
    slug = models.CharField(max_length=40, default=random_slug, unique=True)
    document_name = models.CharField(blank=True, max_length=50)
    document_text = models.TextField(blank=True)
    is_active = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class TermsOfUsePeriod(models.Model):
    document = models.ForeignKey(
        TermsOfUseDocument,
        on_delete=models.SET_NULL,
        null=True,
        related_name="periods",
    )
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)
