from django.http import Http404
from django.shortcuts import render

from .models import TermsOfUseDocument


def terms_of_use_document_view(request):
    document = TermsOfUseDocument.objects.last()
    if not TermsOfUseDocument:
        raise Http404("No document were found")

    return render(request, "termsofuse/document.html", {"document": document})
