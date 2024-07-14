from django.apps import AppConfig


class RoutinesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'routines'

    def ready(self):
        import routines.signals