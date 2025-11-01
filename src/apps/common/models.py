from django.db import models
from django.utils.translation import gettext_lazy as _


class ContactSubmission(models.Model):
    STATUS_CHOICES = [
        ("new", _("Новое")),
        ("in_progress", _("В обработке")),
        ("completed", _("Завершено")),
        ("spam", _("Спам")),
    ]

    name = models.CharField(max_length=100, verbose_name=_("Имя"))
    email = models.EmailField(verbose_name=_("Email"))
    subject = models.CharField(max_length=200, verbose_name=_("Тема"))
    message = models.TextField(verbose_name=_("Сообщение"))
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="new", verbose_name=_("Статус")
    )
    admin_notes = models.TextField(blank=True, verbose_name=_("Заметки администратора"))
    ip_address = models.GenericIPAddressField(
        null=True, blank=True, verbose_name=_("IP адрес")
    )
    user_agent = models.TextField(blank=True, verbose_name=_("User Agent"))
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_("Дата создания")
    )
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Дата обновления"))

    class Meta:
        verbose_name = _("Форма обратной связи")
        verbose_name_plural = _("Формы обратной связи")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} - {self.subject} - {self.created_at.strftime('%d.%m.%Y %H:%M')}"
