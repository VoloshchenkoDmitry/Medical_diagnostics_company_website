from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ServicesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.services'
    verbose_name = _('Услуги')

    def ready(self):
        # Импортируем сигналы для услуг
        try:
            import apps.services.signals
        except ImportError:
            pass