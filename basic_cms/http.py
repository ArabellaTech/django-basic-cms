"""Page CMS functions related to the ``request`` object."""
from . import settings

from django.core.handlers.base import BaseHandler
from django.core.handlers.wsgi import WSGIRequest

from io import StringIO

LANGUAGE_KEYS = [key for (key, value) in settings.PAGE_LANGUAGES]


# TODO In Django 1.3 there is a new RequestFactory class
# that can replace the following function.
def get_request_mock():
    """Build a ``request`` mock up that is used in to render
    the templates in the most fidel environement as possible.

    This fonction is used in the get_placeholders method to
    render the input template and search for the placeholder
    within.
    """
    basehandler = BaseHandler()
    basehandler.load_middleware()
    # http://www.python.org/dev/peps/pep-0333/
    request = WSGIRequest({
        'HTTP_COOKIE': '',
        'PATH_INFO': '/',
        'QUERY_STRING': '',
        'REMOTE_ADDR': '127.0.0.1',
        'REQUEST_METHOD': 'GET',
        'SERVER_NAME': 'page-request-mock',
        'SCRIPT_NAME': '',
        'SERVER_PORT': '80',
        'SERVER_PROTOCOL': 'HTTP/1.1',
        'HTTP_HOST': 'page-request-host',
        'CONTENT_TYPE': 'text/html; charset=utf-8',
        'wsgi.version': (1, 0),
        'wsgi.url_scheme': 'http',
        'wsgi.multiprocess': True,
        'wsgi.multithread': False,
        'wsgi.run_once': False,
        'wsgi.input': StringIO()
    })
    # Apply request middleware
    for middleware_method in basehandler._request_middleware:
        # LocaleMiddleware should never be applied a second time because
        # it would broke the current real request language
        if 'LocaleMiddleware' not in str(middleware_method.__class__):
            middleware_method(request)

    return request


def pages_view(view):
    """
    Make sure the decorated view gets the essential pages
    variables.
    """
    def pages_view_decorator(request, *args, **kwargs):
        # if the current page is already there
        if(kwargs.get('current_page', False) or
                kwargs.get('pages_navigation', False)):
            return view(request, *args, **kwargs)

        path = kwargs.pop('path', None)
        lang = kwargs.pop('lang', None)
        if path:
            from basic_cms.views import details
            response = details(request, path=path, lang=lang,
                only_context=True, delegation=False)
            context = response
            extra_context_var = kwargs.pop('extra_context_var', None)
            if extra_context_var:
                kwargs.update({extra_context_var: context})
            else:
                kwargs.update(context)
        return view(request, *args, **kwargs)
    return pages_view_decorator


def get_slug(path):
    """
    Return the page's slug

        >>> get_slug('/test/function/')
        function
    """
    if path.endswith('/'):
        path = path[:-1]
    return path.split("/")[-1]


def remove_slug(path):
    """
    Return the remainin part of the path

        >>> remove_slug('/test/some/function/')
        test/some
    """
    if path.endswith('/'):
        path = path[:-1]
    if path.startswith('/'):
        path = path[1:]
    if "/" not in path or not path:
        return None
    parts = path.split("/")[:-1]
    return "/".join(parts)


def get_template_from_request(request, page=None):
    """
    Gets a valid template from different sources or falls back to the
    default template.
    """
    page_templates = settings.get_page_templates()
    if len(page_templates) == 0:
        return settings.PAGE_DEFAULT_TEMPLATE
    template = request.REQUEST.get('template', None)
    if template is not None and \
            (template in dict(page_templates).keys() or
            template == settings.PAGE_DEFAULT_TEMPLATE):
        return template
    if page is not None:
        return page.get_template()
    return settings.PAGE_DEFAULT_TEMPLATE


def get_language_from_request(request):
    """Return the most obvious language according the request."""
    language = request.GET.get('language', None)
    if language:
        return language

    if hasattr(request, 'LANGUAGE_CODE'):
        lang = settings.PAGE_LANGUAGE_MAPPING(str(request.LANGUAGE_CODE))
        if lang not in LANGUAGE_KEYS:
            return settings.PAGE_DEFAULT_LANGUAGE
        else:
            return lang
    else:
        return settings.PAGE_DEFAULT_LANGUAGE
