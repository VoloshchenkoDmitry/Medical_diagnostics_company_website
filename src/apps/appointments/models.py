import datetime

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Appointment(models.Model):
    STATUS_CHOICES = [
        ("pending", _("Ожидание подтверждения")),
        ("confirmed", _("Подтверждено")),
        ("completed", _("Завершено")),
        ("cancelled", _("Отменено")),
        ("no_show", _("Не явился")),
    ]

    TIME_SLOTS = [
        ("08:00", "08:00 - 08:30"),
        ("08:30", "08:30 - 09:00"),
        ("09:00", "09:00 - 09:30"),
        ("09:30", "09:30 - 10:00"),
        ("10:00", "10:00 - 10:30"),
        ("10:30", "10:30 - 11:00"),
        ("11:00", "11:00 - 11:30"),
        ("11:30", "11:30 - 12:00"),
        ("12:00", "12:00 - 12:30"),
        ("12:30", "12:30 - 13:00"),
        ("13:00", "13:00 - 13:30"),
        ("13:30", "13:30 - 14:00"),
        ("14:00", "14:00 - 14:30"),
        ("14:30", "14:30 - 15:00"),
        ("15:00", "15:00 - 15:30"),
        ("15:30", "15:30 - 16:00"),
        ("16:00", "16:00 - 16:30"),
        ("16:30", "16:30 - 17:00"),
        ("17:00", "17:00 - 17:30"),
        ("17:30", "17:30 - 18:00"),
        ("18:00", "18:00 - 18:30"),
        ("18:30", "18:30 - 19:00"),
        ("19:00", "19:00 - 19:30"),
        ("19:30", "19:30 - 20:00"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="appointments",
        verbose_name=_("Пользователь"),
    )
    service = models.ForeignKey(
        "services.Service",
        on_delete=models.CASCADE,
        related_name="appointments",
        verbose_name=_("Услуга"),
    )
    desired_date = models.DateField(verbose_name=_("Желаемая дата"))
    desired_time = models.CharField(max_length=5, choices=TIME_SLOTS, verbose_name=_("Желаемое время"))
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
        verbose_name=_("Статус"),
    )
    patient_name = models.CharField(max_length=200, verbose_name=_("Имя пациента"))
    patient_phone = models.CharField(max_length=20, verbose_name=_("Телефон пациента"))
    patient_email = models.EmailField(verbose_name=_("Email пациента"))
    patient_age = models.PositiveIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(120)],
        verbose_name=_("Возраст пациента"),
    )
    comments = models.TextField(blank=True, verbose_name=_("Комментарий"))
    admin_notes = models.TextField(blank=True, verbose_name=_("Заметки администратора"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Дата создания"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Дата обновления"))

    class Meta:
        verbose_name = _("Запись на прием")
        verbose_name_plural = _("Записи на прием")
        ordering = ["-desired_date", "desired_time"]
        constraints = [models.UniqueConstraint(fields=["desired_date", "desired_time"], name="unique_appointment_time")]

    def __str__(self):
        return f"{self.patient_name} - {self.service.name} - {self.desired_date} {self.desired_time}"

    @property
    def is_past_due(self):
        """Проверяет, прошла ли дата приема"""
        appointment_datetime = datetime.datetime.combine(
            self.desired_date,
            datetime.datetime.strptime(self.desired_time, "%H:%M").time(),
        )
        return timezone.now() > timezone.make_aware(appointment_datetime)

    @property
    def can_be_cancelled(self):
        """Можно ли отменить запись"""
        return self.status in ["pending", "confirmed"] and not self.is_past_due

    @property
    def formatted_time(self):
        """Форматированное время"""
        return dict(self.TIME_SLOTS).get(self.desired_time, self.desired_time)

    def get_status_color(self):
        """Цвет статуса для отображения"""
        colors = {
            "pending": "warning",
            "confirmed": "success",
            "completed": "info",
            "cancelled": "danger",
            "no_show": "secondary",
        }
        return colors.get(self.status, "secondary")


class AppointmentResult(models.Model):
    appointment = models.OneToOneField(
        Appointment,
        on_delete=models.CASCADE,
        related_name="result",
        verbose_name=_("Запись на прием"),
    )
    diagnosis = models.TextField(verbose_name=_("Диагноз"))
    recommendations = models.TextField(verbose_name=_("Рекомендации"))
    prescription = models.TextField(blank=True, verbose_name=_("Назначения"))
    results_file = models.FileField(
        upload_to="appointment_results/",
        blank=True,
        null=True,
        verbose_name=_("Файл с результатами"),
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Дата создания"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Дата обновления"))

    class Meta:
        verbose_name = _("Результат приема")
        verbose_name_plural = _("Результаты приемов")

    def __str__(self):
        return f"Результат приема {self.appointment}"
