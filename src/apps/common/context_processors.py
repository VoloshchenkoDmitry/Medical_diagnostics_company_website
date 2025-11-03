from django.conf import settings
from django.utils.translation import gettext_lazy as _


def site_info(request):
    """
    Контекстный процессор для добавления информации о сайте во все шаблоны
    """
    return {
        "SITE_NAME": getattr(settings, "SITE_NAME", "Медицинский Диагностический Центр"),
        "SITE_DESCRIPTION": getattr(
            settings,
            "SITE_DESCRIPTION",
            "Современная диагностика и качественное лечение",
        ),
        "CONTACT_PHONE": getattr(settings, "CONTACT_PHONE", "+7 (495) 123-45-67"),
        "CONTACT_EMAIL": getattr(settings, "CONTACT_EMAIL", "info@medical-center.ru"),
        "SITE_ADDRESS": getattr(settings, "SITE_ADDRESS", "г. Москва, ул. Медицинская, д. 15"),
    }
