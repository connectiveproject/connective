from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import TermsOfUseDocument, TermsOfUsePeriod


@receiver(post_save, sender=TermsOfUseDocument)
def on_document_activation(sender, instance, created, **kwargs):
    """
    if doc changed to active, dis-activate all other docs & add new period record
    """
    # exit if doc was not changed to active in current `save`
    if (
        not instance.is_active
        or TermsOfUsePeriod.objects.filter(
            document=instance, end_date__isnull=True
        ).exists()
    ):
        return

    previous_active_docs = sender.objects.filter(is_active=True).exclude(
        slug=instance.slug
    )
    previous_active_docs.update(is_active=False)
    TermsOfUsePeriod.objects.create(document=instance)


@receiver(post_save, sender=TermsOfUsePeriod)
def close_previous_periods_on_creation(sender, instance, created, **kwargs):
    """
    on period creation, close previous periods (assign end time)
    """
    if created and instance.end_date is None:
        periods_to_close = sender.objects.filter(end_date__isnull=True).exclude(
            pk=instance.pk
        )
        periods_to_close.update(end_date=instance.start_date)
