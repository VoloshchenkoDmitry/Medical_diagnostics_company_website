from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class Appointment(models.Model):
    """Модель записи на прием"""

    STATUS_CHOICES = [
        ('pending', _('Ожидание подтверждения')),
        ('confirmed', _('Подтверждено')),
        ('completed', _('Выполнено')),
        ('cancelled', _('Отменено')),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='appointments',
        verbose_name=_('Пользователь')
    )
    service = models.ForeignKey(
        'services.Service',
        on_delete=models.CASCADE,
        related_name='appointments',
        verbose_name=_('Услуга')
    )
    desired_date = models.DateField(verbose_name=_('Желаемая дата'))
    desired_time = models.TimeField(verbose_name=_('Желаемое время'))
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name=_('Статус')
    )
    notes = models.TextField(blank=True, verbose_name=_('Комментарий'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Дата создания'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Дата обновления'))

    class Meta:
        verbose_name = _('Запись на прием')
        verbose_name_plural = _('Записи на прием')
        ordering = ['-desired_date', '-desired_time']

    def __str__(self):
        return f"{self.user} - {self.service} - {self.desired_date}"