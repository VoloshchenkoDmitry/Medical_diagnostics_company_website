from django.db import models
from django.utils.text import slugify


class ServiceCategory(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название категории')
    description = models.TextField(blank=True, verbose_name='Описание')
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок отображения')

    class Meta:
        verbose_name = 'Категория услуг'
        verbose_name_plural = 'Категории услуг'
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class Service(models.Model):
    category = models.ForeignKey(
        ServiceCategory,
        on_delete=models.CASCADE,
        related_name='services',
        verbose_name='Категория'
    )
    name = models.CharField(max_length=200, verbose_name='Название услуги')
    slug = models.SlugField(max_length=200, unique=True, verbose_name='URL')
    description = models.TextField(verbose_name='Описание')
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Цена'
    )
    image = models.ImageField(
        upload_to='services/',
        blank=True,
        null=True,
        verbose_name='Изображение'
    )
    is_active = models.BooleanField(default=True, verbose_name='Активна')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'
        ordering = ['category', 'name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)