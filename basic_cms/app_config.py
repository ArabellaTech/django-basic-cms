from django.apps import AppConfig


class BasicCmsConfig(AppConfig):
    name = 'basic_cms'

    def ready(self):
        from . import checks
