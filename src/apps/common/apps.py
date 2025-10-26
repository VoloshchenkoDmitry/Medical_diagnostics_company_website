from django.apps import AppConfig


class CommonConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.common'
    verbose_name = 'Общие страницы'

    def ready(self):
        # Импортируем сигналы, если они будут
        try:
            import apps.common.signals
        except ImportError:
            pass