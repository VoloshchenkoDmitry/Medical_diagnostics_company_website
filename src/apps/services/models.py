from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _


class ServiceCategory(models.Model):
    name = models.CharField(max_length=200, verbose_name=_('Название категории'))
    slug = models.SlugField(max_length=200, unique=True, verbose_name=_('URL'))
    description = models.TextField(blank=True, verbose_name=_('Описание'))
    order = models.PositiveIntegerField(default=0, verbose_name=_('Порядок отображения'))
    # Добавляем поля created_at и updated_at
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Дата создания'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Дата обновления'))

    class Meta:
        verbose_name = _('Категория услуг')
        verbose_name_plural = _('Категории услуг')
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Service(models.Model):
    category = models.ForeignKey(
        ServiceCategory,
        on_delete=models.CASCADE,
        related_name='services',
        verbose_name=_('Категория')
    )
    name = models.CharField(max_length=200, verbose_name=_('Название услуги'))
    slug = models.SlugField(max_length=200, unique=True, verbose_name=_('URL'))
    description = models.TextField(verbose_name=_('Описание'))
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_('Цена')
    )
    image = models.ImageField(
        upload_to='services/',
        blank=True,
        null=True,
        verbose_name=_('Изображение')
    )
    is_active = models.BooleanField(default=True, verbose_name=_('Активна'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Дата создания'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Дата обновления'))

    class Meta:
        verbose_name = _('Услуга')
        verbose_name_plural = _('Услуги')
        ordering = ['category', 'name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)