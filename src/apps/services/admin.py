from django.contrib import admin
from .models import ServiceCategory, Service


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'order', 'services_count')
    list_editable = ('order',)
    search_fields = ('name', 'description')
    prepopulated_fields = {'description': ('name',)}

    def services_count(self, obj):
        return obj.services.count()

    services_count.short_description = 'Количество услуг'


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'is_active', 'created_at')
    list_filter = ('category', 'is_active', 'created_at')
    search_fields = ('name', 'description')
    list_editable = ('price', 'is_active')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Основная информация', {
            'fields': ('category', 'name', 'slug', 'description')
        }),
        ('Детали', {
            'fields': ('price', 'image', 'is_active')
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )