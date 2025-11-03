from django.contrib import admin, messages
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from .models import Service, ServiceCategory


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "order", "service_count", "is_active"]
    list_editable = ["order"]
    list_filter = ["created_at"]  # Исправлено - поле существует в модели
    search_fields = ["name", "description"]
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ["created_at", "updated_at"]  # Теперь поля существуют в модели

    fieldsets = (
        (None, {"fields": ("name", "slug", "description", "order")}),
        (
            _("Дополнительная информация"),
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )

    def service_count(self, obj):
        return obj.services.count()

    service_count.short_description = _("Количество услуг")

    def is_active(self, obj):
        return obj.services.filter(is_active=True).exists()

    is_active.boolean = True
    is_active.short_description = _("Есть активные услуги")


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "category",
        "price",
        "is_active",
        "image_preview",
        "created_at",
    ]
    list_filter = ["category", "is_active", "created_at", "updated_at"]
    list_editable = ["price", "is_active"]
    search_fields = ["name", "description", "category__name"]
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ["created_at", "updated_at", "image_preview_large"]
    date_hierarchy = "created_at"

    fieldsets = (
        (
            _("Основная информация"),
            {"fields": ("name", "slug", "category", "description", "price")},
        ),
        (_("Изображение"), {"fields": ("image", "image_preview_large")}),
        (_("Статус"), {"fields": ("is_active",)}),
        (_("Даты"), {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}),
    )

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="50" height="50" style="object-fit: cover;" />',
                obj.image.url,
            )
        return "—"

    image_preview.short_description = _("Изображение")

    def image_preview_large(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="200" style="object-fit: cover; border-radius: 8px;" />',
                obj.image.url,
            )
        return _("Изображение не загружено")

    image_preview_large.short_description = _("Предпросмотр изображения")

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("category")

    # Действия в админке
    actions = ["activate_services", "deactivate_services"]

    def activate_services(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, _("Активировано {} услуг").format(updated), messages.SUCCESS)

    activate_services.short_description = _("Активировать выбранные услуги")

    def deactivate_services(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, _("Деактивировано {} услуг").format(updated), messages.SUCCESS)

    deactivate_services.short_description = _("Деактивировать выбранные услуги")
