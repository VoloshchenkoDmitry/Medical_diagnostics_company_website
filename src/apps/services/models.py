from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _


class ServiceCategory(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название категории")
    slug = models.SlugField(max_length=200, unique=True, blank=True, verbose_name="URL")
    description = models.TextField(blank=True, verbose_name="Описание")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок отображения")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Категория услуг"
        verbose_name_plural = "Категории услуг"
        ordering = ["order", "name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Для нового объекта или если slug пустой
        if not self.slug or self._state.adding:
            self.slug = self._generate_slug(self.name)
        else:
            # Для существующего объекта проверяем, изменилось ли имя
            try:
                old_obj = ServiceCategory.objects.get(pk=self.pk)
                if old_obj.name != self.name:
                    self.slug = self._generate_slug(self.name)
            except ServiceCategory.DoesNotExist:
                # Если объекта нет в базе (маловероятно), генерируем slug
                self.slug = self._generate_slug(self.name)

        super().save(*args, **kwargs)

    def _generate_slug(self, text):
        """Генерирует slug из текста с поддержкой кириллицы"""
        # Упрощенная транслитерация для кириллицы (более стандартная)
        translit_map = {
            "а": "a",
            "б": "b",
            "в": "v",
            "г": "g",
            "д": "d",
            "е": "e",
            "ё": "e",
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
            "х": "kh",
            "ц": "c",  # 'ц' -> 'c'
            "ч": "ch",
            "ш": "sh",
            "щ": "shch",
            "ъ": "",
            "ы": "y",
            "ь": "",
            "э": "e",
            "ю": "yu",
            "я": "ya",
            " ": "-",
            "-": "-",
        }

        # Транслитерируем текст
        base_slug = ""
        for c in text:
            if c.lower() in translit_map:
                base_slug += translit_map[c.lower()]
            elif c.isalnum():
                base_slug += c.lower()
            elif c == " " or c == "-":
                base_slug += "-"

        base_slug = slugify(base_slug)

        # Проверяем уникальность slug
        original_slug = base_slug
        counter = 1
        model_class = self.__class__

        while model_class.objects.filter(slug=base_slug).exclude(pk=getattr(self, "pk", None)).exists():
            base_slug = f"{original_slug}-{counter}"
            counter += 1

        return base_slug


class Service(models.Model):
    category = models.ForeignKey(
        ServiceCategory,
        on_delete=models.CASCADE,
        related_name="services",
        verbose_name="Категория",
    )
    name = models.CharField(max_length=200, verbose_name="Название услуги")
    slug = models.SlugField(max_length=200, unique=True, blank=True, verbose_name="URL")
    description = models.TextField(verbose_name="Описание")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    image = models.ImageField(upload_to="services/", blank=True, null=True, verbose_name="Изображение")
    is_active = models.BooleanField(default=True, verbose_name="Активна")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"
        ordering = ["category", "name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Для нового объекта или если slug пустой
        if not self.slug or self._state.adding:
            self.slug = self._generate_slug(self.name)
        else:
            # Для существующего объекта проверяем, изменилось ли имя
            try:
                old_obj = Service.objects.get(pk=self.pk)
                if old_obj.name != self.name:
                    self.slug = self._generate_slug(self.name)
            except Service.DoesNotExist:
                # Если объекта нет в базе (маловероятно), генерируем slug
                self.slug = self._generate_slug(self.name)

        super().save(*args, **kwargs)

    def _generate_slug(self, text):
        """Генерирует slug из текста с поддержкой кириллицы"""
        # Упрощенная транслитерация для кириллицы (более стандартная)
        translit_map = {
            "а": "a",
            "б": "b",
            "в": "v",
            "г": "g",
            "д": "d",
            "е": "e",
            "ё": "e",
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
            "х": "kh",
            "ц": "c",  # 'ц' -> 'c'
            "ч": "ch",
            "ш": "sh",
            "щ": "shch",
            "ъ": "",
            "ы": "y",
            "ь": "",
            "э": "e",
            "ю": "yu",
            "я": "ya",
            " ": "-",
            "-": "-",
        }

        # Транслитерируем текст
        base_slug = ""
        for c in text:
            if c.lower() in translit_map:
                base_slug += translit_map[c.lower()]
            elif c.isalnum():
                base_slug += c.lower()
            elif c == " " or c == "-":
                base_slug += "-"

        base_slug = slugify(base_slug)

        # Проверяем уникальность slug
        original_slug = base_slug
        counter = 1
        model_class = self.__class__

        while model_class.objects.filter(slug=base_slug).exclude(pk=getattr(self, "pk", None)).exists():
            base_slug = f"{original_slug}-{counter}"
            counter += 1

        return base_slug
