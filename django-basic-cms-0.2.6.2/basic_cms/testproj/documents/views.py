from django.template import RequestContext
from django.shortcuts import render_to_response
from basic_cms.testproj.documents.models import Document


def document_view(request, *args, **kwargs):
    context = RequestContext(request, kwargs)
    if kwargs.get('current_page', False):
        documents = Document.objects.filter(page=kwargs['current_page'])
        context['documents'] = documents
    if 'document_id' in kwargs:
        document = Document.objects.get(pk=int(kwargs['document_id']))
        context['document'] = document
    context['in_document_view'] = True
    return render_to_response('pages/examples/index.html', context, context_instance=RequestContext(request))
