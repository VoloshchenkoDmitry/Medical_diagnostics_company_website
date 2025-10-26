from django.contrib import admin
from .models import Appointment


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'service', 'desired_date', 'desired_time', 'status', 'created_at')
    list_filter = ('status', 'desired_date', 'service', 'created_at')
    search_fields = ('user__username', 'user__email', 'service__name', 'notes')
    list_editable = ('status',)
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'desired_date'

    fieldsets = (
        ('Основная информация', {
            'fields': ('user', 'service', 'status')
        }),
        ('Дата и время', {
            'fields': ('desired_date', 'desired_time')
        }),
        ('Дополнительно', {
            'fields': ('notes', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )