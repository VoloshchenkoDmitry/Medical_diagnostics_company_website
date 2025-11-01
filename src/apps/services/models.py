from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator
import unicodedata
import re


from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _


def custom_slugify(value):
    """Кастомная функция для slugify с поддержкой кириллицы"""
    value = str(value)
    # Транслитерация кириллицы в латиницу
    translit_map = {
        "а": "a",
        "б": "b",
        "в": "v",
        "г": "g",
        "д": "d",
        "е": "e",
        "ё": "yo",
        "ж": "zh",
        "з": "z",
        "и": "i",
        "й": "y",
        "к": "k",
        "л": "l",
        "м": "m",
        "н": "n",
        "о": "o",
        "п": "p",
        "р": "r",
        "с": "s",
        "т": "t",
        "у": "u",
        "ф": "f",
        "х": "h",
        "ц": "ts",
        "ч": "ch",
        "ш": "sh",
        "щ": "sch",
        "ъ": "",
        "ы": "y",
        "ь": "",
        "э": "e",
        "ю": "yu",
        "я": "ya",
        "А": "A",
        "Б": "B",
        "В": "V",
        "Г": "G",
        "Д": "D",
        "Е": "E",
        "Ё": "Yo",
        "Ж": "Zh",
        "З": "Z",
        "И": "I",
        "Й": "Y",
        "К": "K",
        "Л": "L",
        "М": "M",
        "Н": "N",
        "О": "O",
        "П": "P",
        "Р": "R",
        "С": "S",
        "Т": "T",
        "У": "U",
        "Ф": "F",
        "Х": "H",
        "Ц": "Ts",
        "Ч": "Ch",
        "Ш": "Sh",
        "Щ": "Sch",
        "Ъ": "",
        "Ы": "Y",
        "Ь": "",
        "Э": "E",
        "Ю": "Yu",
        "Я": "Ya",
    }

    # Транслитерация
    result = []
    for char in value:
        result.append(translit_map.get(char, char))
    value = "".join(result)

    # Стандартный slugify
    value = (
        unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    )
    value = re.sub(r"[^\w\s-]", "", value.lower())
    return re.sub(r"[-\s]+", "-", value).strip("-_")


class ServiceCategory(models.Model):
    name = models.CharField(max_length=200, verbose_name=_("Название категории"))
    slug = models.SlugField(
        max_length=200, unique=True, verbose_name=_("URL"), blank=True
    )
    description = models.TextField(blank=True, verbose_name=_("Описание"))
    order = models.PositiveIntegerField(
        default=0, verbose_name=_("Порядок отображения")
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_("Дата создания")
    )
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Дата обновления"))

    class Meta:
        verbose_name = _("Категория услуг")
        verbose_name_plural = _("Категории услуг")
        ordering = ["order", "name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Генерируем slug только если он пустой
        if not self.slug and self.name:
            self.slug = custom_slugify(self.name)
            # Добавляем суффикс если slug уже существует
            counter = 1
            original_slug = self.slug
            while (
                ServiceCategory.objects.filter(slug=self.slug)
                .exclude(pk=self.pk)
                .exists()
            ):
                self.slug = f"{original_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)


class Service(models.Model):
    category = models.ForeignKey(
        ServiceCategory,
        on_delete=models.CASCADE,
        related_name="services",
        verbose_name=_("Категория"),
    )
    name = models.CharField(max_length=200, verbose_name=_("Название услуги"))
    slug = models.SlugField(
        max_length=200, unique=True, verbose_name=_("URL"), blank=True
    )
    description = models.TextField(
        verbose_name=_("Описание"), default=""
    )  # Добавляем default
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Цена"),
        validators=[MinValueValidator(0.01)],
    )
    image = models.ImageField(
        upload_to="services/", blank=True, null=True, verbose_name=_("Изображение")
    )
    is_active = models.BooleanField(default=True, verbose_name=_("Активна"))
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_("Дата создания")
    )
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Дата обновления"))

    class Meta:
        verbose_name = _("Услуга")
        verbose_name_plural = _("Услуги")
        ordering = ["category", "name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Генерируем slug только если он пустой
        if not self.slug and self.name:
            self.slug = custom_slugify(self.name)
            # Добавляем суффикс если slug уже существует
            counter = 1
            original_slug = self.slug
            while Service.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)
