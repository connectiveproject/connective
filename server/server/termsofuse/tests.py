from contextlib import suppress

import pytest
from django.core.exceptions import ValidationError

from .models import TermsOfUseDocument, TermsOfUsePeriod

pytestmark = pytest.mark.django_db


class TestTermsofuseSignals:
    def test_on_document_activation(self):
        """
        make sure period record is created & is_active is True for one object only
        """
        doc_1 = TermsOfUseDocument.objects.create(document_name="1", is_active=True)
        doc_2 = TermsOfUseDocument.objects.create(document_name="2", is_active=True)
        doc_1.refresh_from_db()

        doc_1_period = TermsOfUsePeriod.objects.get(document=doc_1)
        doc_2_period = TermsOfUsePeriod.objects.get(document=doc_2)

        assert not doc_1.is_active
        assert doc_2.is_active
        assert doc_1_period.end_date == doc_2_period.start_date
        assert doc_2_period.end_date is None

    def test_at_least_one_active_doc(self):
        """
        make sure there is at least one active terms-of-use doc
        """
        doc = TermsOfUseDocument.objects.create(document_name="1", is_active=True)
        TermsOfUseDocument.objects.create(document_name="2", is_active=False)
        doc.is_active = False
        with suppress(ValidationError):
            doc.save()
            assert False
