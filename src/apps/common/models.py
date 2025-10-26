from django.db import models
from django.utils.translation import gettext_lazy as _


class Contact(models.Model):
    """Модель для контактной информации"""
    name = models.CharField(max_length=100, verbose_name=_('Имя'))
    email = models.EmailField(verbose_name=_('Email'))
    phone = models.CharField(max_length=20, verbose_name=_('Телефон'))
    address = models.TextField(verbose_name=_('Адрес'))
    map_code = models.TextField(
        blank=True,
        verbose_name=_('Код карты'),
        help_text=_('HTML код для вставки карты')
    )
    is_active = models.BooleanField(default=True, verbose_name=_('Активный'))
    order = models.PositiveIntegerField(default=0, verbose_name=_('Порядок'))

    class Meta:
        verbose_name = _('Контакт')
        verbose_name_plural = _('Контакты')
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class SiteSetting(models.Model):
    """Модель для настроек сайта"""
    key = models.CharField(max_length=100, unique=True, verbose_name=_('Ключ'))
    value = models.TextField(verbose_name=_('Значение'))
    description = models.TextField(blank=True, verbose_name=_('Описание'))

    class Meta:
        verbose_name = _('Настройка сайта')
        verbose_name_plural = _('Настройки сайта')

    def __str__(self):
        return self.key