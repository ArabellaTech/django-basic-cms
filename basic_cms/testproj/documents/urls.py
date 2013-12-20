from django.conf.urls import *
from basic_cms.testproj.documents.views import document_view
from basic_cms.http import pages_view

urlpatterns = patterns('',
    url(r'^doc-(?P<document_id>[0-9]+)$', pages_view(document_view), name='document_details'),
    url(r'^$', pages_view(document_view), name='document_root'),
)
