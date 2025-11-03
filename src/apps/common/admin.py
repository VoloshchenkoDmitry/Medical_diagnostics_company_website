from django.contrib import admin
from django.urls import reverse
from django.utils import timezone
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _


class MedicalAdminSite(admin.AdminSite):
    site_header = _("Панель управления Медицинским Диагностическим Центром")
    site_title = _("Администрирование МДЦ")
    index_title = _("Добро пожаловать в панель управления")


# Кастомная главная страница админки
def custom_admin_index(request):
    from django.contrib.admin import AdminSite

    from apps.appointments.models import Appointment
    from apps.services.models import Service, ServiceCategory
    from apps.users.models import User

    # Статистика для главной страницы админки
    stats = {
        "total_users": User.objects.count(),
        "total_services": Service.objects.count(),
        "total_categories": ServiceCategory.objects.count(),
        "total_appointments": Appointment.objects.count(),
        "pending_appointments": Appointment.objects.filter(status="pending").count(),
        "today_appointments": Appointment.objects.filter(desired_date=timezone.now().date()).count(),
        "new_users_today": User.objects.filter(date_joined__date=timezone.now().date()).count(),
    }

    # Быстрые ссылки
    quick_links = [
        {
            "title": _("Добавить услугу"),
            "url": reverse("admin:services_service_add"),
            "icon": "fas fa-plus",
            "color": "success",
        },
        {
            "title": _("Просмотреть записи"),
            "url": reverse("admin:appointments_appointment_changelist"),
            "icon": "fas fa-calendar-alt",
            "color": "info",
        },
        {
            "title": _("Управление пользователями"),
            "url": reverse("admin:users_user_changelist"),
            "icon": "fas fa-users",
            "color": "warning",
        },
        {
            "title": _("Добавить категорию"),
            "url": reverse("admin:services_servicecategory_add"),
            "icon": "fas fa-folder-plus",
            "color": "primary",
        },
    ]

    return admin.site.__class__.index(admin.site, request, extra_context={"stats": stats, "quick_links": quick_links})


# Применяем кастомную главную страницу
admin.site.index = custom_admin_index

# Кастомный шаблон для главной страницы админки
admin.site.index_template = "admin/custom_index.html"
