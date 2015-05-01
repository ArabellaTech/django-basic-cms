"""Django haystack `SearchIndex` module."""
from basic_cms.models import Page

from haystack.indexes import SearchIndex, CharField, DateTimeField, Indexable


class PageIndex(SearchIndex, Indexable):
    """Search index for pages content."""
    text = CharField(document=True, use_template=True)
    title = CharField(model_attr='title')
    url = CharField(model_attr='get_absolute_url')
    publication_date = DateTimeField(model_attr='publication_date')

    def index_queryset(self, using=None):
        return self.get_model().objects.published()

    def should_update(self, instance, **kwargs):
        return instance.status == Page.PUBLISHED

    def get_model(self):
        return Page
