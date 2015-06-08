from basic_cms.models import Page

from django.template.loader import render_to_string
from django.utils.translation import get_language
from django.http import Http404
from django.utils.safestring import mark_safe
from django.utils.functional import lazy
from django.template import RequestContext

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from basic_cms.utils import links_append_domain

mark_safe_lazy = lazy(mark_safe)


class BasicCMSAPI(APIView):
    """
    Get basic cms page by slug in given format

    format -- json/html, html = default
    get-children -- true/false, true by default, works only with json.

    """

    permission_classes = (AllowAny,)

    def get(self, request, slug, *args, **kwargs):
        format = request.GET.get('format', 'html')
        get_children = request.GET.get('get-children', True)
        lang = get_language()
        page = Page.objects.from_path(slug, lang)
        if page is None:
            raise Http404("Page does not exist")

        if format == 'html':
            page = render_to_string(page.template, {'current_page': page})
            base_url = request.build_absolute_uri('/')
            return Response({"html": links_append_domain(page, base_url)})
        else:
            page = page.dump_json_data(get_children=get_children)
            return Response(page)
