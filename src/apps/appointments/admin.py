from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Appointment, AppointmentResult


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = [
        'patient_name',
        'service',
        'desired_date',
        'desired_time',
        'status',
        'created_at'
    ]
    list_filter = [
        'status',
        'desired_date',
        'service__category',
        'created_at'
    ]
    search_fields = [
        'patient_name',
        'patient_phone',
        'patient_email',
        'service__name',
        'user__username',
        'user__email'
    ]
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'desired_date'

    fieldsets = (
        (_('Основная информация'), {
            'fields': (
                'user', 'service', 'status',
                'desired_date', 'desired_time'
            )
        }),
        (_('Информация о пациенте'), {
            'fields': (
                'patient_name', 'patient_phone', 'patient_email',
                'patient_age', 'comments'
            )
        }),
        (_('Административная информация'), {
            'fields': ('admin_notes', 'created_at', 'updated_at')
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'service', 'service__category')


@admin.register(AppointmentResult)
class AppointmentResultAdmin(admin.ModelAdmin):
    list_display = ['appointment', 'created_at']
    list_filter = ['created_at']
    search_fields = [
        'appointment__patient_name',
        'appointment__service__name',
        'diagnosis'
    ]
    readonly_fields = ['created_at', 'updated_at']