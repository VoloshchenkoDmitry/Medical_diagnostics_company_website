from django.contrib.admin import AdminSite
from django.utils.translation import gettext_lazy as _


class MedicalAdminSite(AdminSite):
    site_header = _("Панель управления медицинским центром")
    site_title = _("Администрирование медицинского центра")
    index_title = _("Панель управления")


# Создаем экземпляр кастомной админки
medical_admin_site = MedicalAdminSite(name="medical_admin")
