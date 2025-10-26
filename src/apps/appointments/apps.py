from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AppointmentsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.appointments'
    verbose_name = _('Записи на прием')

    def ready(self):
        # Импортируем сигналы для записей
        try:
            import apps.appointments.signals
        except ImportError:
            pass