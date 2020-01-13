
from importlib import import_module
from django.conf.urls import include, url
from django.contrib import admin
from basic_cms.views import PageSitemap, MultiLanguagePageSitemap


admin.autodiscover()

urlpatterns = [
    url(r'^i18n/', include('django.conf.urls.i18n')),

    url(r'^pages/', include('basic_cms.urls')),

    # this is only used to enable the reverse url to work with documents
    url(r'^pages/(?P<path>.*)', include('basic_cms.testproj.documents.urls')),

    url(r'^admin/', include(admin.site.urls)),
    # make tests fail if a backend is not present on the system
    #(r'^search/', include('haystack.urls')),
]

try:
    sitemaps_mod = import_module('django.contrib.sitemaps.views')
    urlpatterns += [
        url(r'^sitemap\.xml$', getattr(sitemaps_mod, 'sitemap'),
            {'sitemaps': {'pages': PageSitemap}}),

        url(r'^sitemap2\.xml$', getattr(sitemaps_mod, 'sitemap'),
            {'sitemaps': {'pages': MultiLanguagePageSitemap}})
    ]
except:
    raise
