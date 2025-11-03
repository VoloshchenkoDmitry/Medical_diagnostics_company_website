from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    GENDER_CHOICES = [
        ("M", _("Мужской")),
        ("F", _("Женский")),
        ("O", _("Другой")),
    ]

    email = models.EmailField(
        _("email address"),
        unique=True,
        error_messages={
            "unique": _("Пользователь с таким email уже существует."),
        },
    )
    phone = models.CharField(max_length=20, blank=True, verbose_name=_("Телефон"))
    date_of_birth = models.DateField(null=True, blank=True, verbose_name=_("Дата рождения"))
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, verbose_name=_("Пол"))
    address = models.TextField(blank=True, verbose_name=_("Адрес"))
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True, verbose_name=_("Аватар"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Дата регистрации"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Дата обновления"))

    class Meta:
        verbose_name = _("Пользователь")
        verbose_name_plural = _("Пользователи")
        ordering = ["-created_at"]

    def __str__(self):
        return self.username

    def get_full_name(self):
        full_name = f"{self.first_name} {self.last_name}"
        return full_name.strip() or self.username
