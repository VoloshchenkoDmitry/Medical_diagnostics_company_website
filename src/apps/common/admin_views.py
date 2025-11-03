import datetime

from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count, Q
from django.shortcuts import render
from django.utils import timezone

from apps.appointments.models import Appointment
from apps.common.models import ContactSubmission
from apps.services.models import Service
from apps.users.models import User


@staff_member_required
def admin_dashboard(request):
    """Кастомная главная страница админки"""

    # Статистика за последние 30 дней
    thirty_days_ago = timezone.now() - datetime.timedelta(days=30)

    # Статистика записей
    total_appointments = Appointment.objects.count()
    recent_appointments = Appointment.objects.filter(created_at__gte=thirty_days_ago).count()
    pending_appointments = Appointment.objects.filter(status="pending").count()

    # Статистика пользователей
    total_users = User.objects.count()
    new_users = User.objects.filter(date_joined__gte=thirty_days_ago).count()

    # Статистика услуг
    total_services = Service.objects.count()
    active_services = Service.objects.filter(is_active=True).count()

    # Статистика обратной связи
    new_contacts = ContactSubmission.objects.filter(status="new").count()
    total_contacts = ContactSubmission.objects.count()

    # Последние записи
    recent_appointments_list = Appointment.objects.select_related("service", "user").order_by("-created_at")[:10]

    # Статистика по статусам записей
    appointment_status_stats = Appointment.objects.values("status").annotate(count=Count("id")).order_by("status")

    context = {
        "title": "Панель управления",
        "total_appointments": total_appointments,
        "recent_appointments": recent_appointments,
        "pending_appointments": pending_appointments,
        "total_users": total_users,
        "new_users": new_users,
        "total_services": total_services,
        "active_services": active_services,
        "new_contacts": new_contacts,
        "total_contacts": total_contacts,
        "recent_appointments_list": recent_appointments_list,
        "appointment_status_stats": appointment_status_stats,
    }

    return render(request, "admin/custom_dashboard.html", context)
