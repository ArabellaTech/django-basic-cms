from django.core.checks import register
from django.core import checks
from django import template
from django.template import loader
from django.conf import settings


@register()
def page_templates_loading_check(app_configs, **kwargs):
    """ Check if any page template can't be loaded. """
    errors = []

    for page_template in settings.PAGE_TEMPLATES:
        try:
            loader.get_template(page_template[0])
        except template.TemplateDoesNotExist:
            errors.append(checks.Warning(
                    'Django cannot find template %s' % page_template[0],
                    obj=page_template, id='basic_cms.W001'))

    return errors
