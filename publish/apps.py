from django.apps import AppConfig


class PublishConfig(AppConfig):
    name = 'publish'

    def ready(self):
        import publish.signals