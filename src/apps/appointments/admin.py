from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.urls import reverse
from .models import Appointment, AppointmentResult


class AppointmentResultInline(admin.StackedInline):
    model = AppointmentResult
    extra = 0
    fields = ['diagnosis', 'recommendations', 'prescription', 'results_file']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = [
        'patient_name',
        'service',
        'desired_date',
        'desired_time',
        'status',
        'status_badge',
        'user_link',
        'created_at',
        'actions',
    ]
    list_filter = [
        'status',
        'desired_date',
        'service__category',
        'created_at',
        'updated_at',
    ]
    search_fields = [
        'patient_name',
        'patient_phone',
        'patient_email',
        'service__name',
        'user__username',
        'user__email',
    ]
    readonly_fields = [
        'created_at',
        'updated_at',
        'user_info',
    ]
    list_editable = ['status']
    date_hierarchy = 'desired_date'
    inlines = [AppointmentResultInline]

    fieldsets = (
        (_('Основная информация'), {
            'fields': (
                'user',
                'user_info',
                'service',
                'status',
                'desired_date',
                'desired_time',
            )
        }),
        (_('Информация о пациенте'), {
            'fields': (
                'patient_name',
                'patient_phone',
                'patient_email',
                'patient_age',
                'comments',
            )
        }),
        (_('Административная информация'), {
            'fields': (
                'admin_notes',
                'created_at',
                'updated_at',
            ),
            'classes': ('collapse',)
        }),
    )

    def status_badge(self, obj):
        colors = {
            'pending': 'warning',
            'confirmed': 'success',
            'completed': 'info',
            'cancelled': 'danger',
            'no_show': 'secondary',
        }
        color = colors.get(obj.status, 'secondary')
        return format_html(
            '<span class="badge bg-{}">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = _('Статус (бейдж)')
    status_badge.admin_order_field = 'status'

    def user_link(self, obj):
        if obj.user:
            url = reverse('admin:users_user_change', args=[obj.user.id])
            return format_html(
                '<a href="{}">{}</a>',
                url,
                obj.user.username
            )
        return "—"
    user_link.short_description = _('Пользователь')

    def user_info(self, obj):
        if obj.user:
            info = (
                "<div style='padding: 10px; background: #f8f9fa; "
                "border-radius: 5px;'>"
                "<strong>Пользователь:</strong> {}<br>"
                "<strong>Email:</strong> {}<br>"
                "<strong>Телефон:</strong> {}<br>"
                "<strong>Дата регистрации:</strong> {}"
                "</div>"
            ).format(
                obj.user.get_full_name() or obj.user.username,
                obj.user.email,
                obj.user.phone or 'Не указан',
                obj.user.date_joined.strftime('%d.%m.%Y'),
            )
            return format_html(info)
        return _("Не зарегистрированный пользователь")
    user_info.short_description = _('Информация о пользователе')

    def actions(self, obj):
        links = []
        if obj.status in ['pending', 'confirmed']:
            url = reverse('admin:appointments_appointment_change', args=[obj.id])
            links.append(
                f'<a href="{url}" class="button">Редактировать</a>'
            )
        return format_html(' '.join(links))
    actions.short_description = _('Действия')

    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'user', 'service', 'service__category'
        )

    # Действия в админке
    actions = [
        'confirm_appointments',
        'complete_appointments',
        'cancel_appointments',
        'mark_as_no_show',
    ]

    def confirm_appointments(self, request, queryset):
        updated = queryset.filter(status='pending').update(status='confirmed')
        self.message_user(
            request,
            _('Подтверждено {} записей').format(updated),
            messages.SUCCESS
        )
    confirm_appointments.short_description = _('Подтвердить выбранные записи')

    def complete_appointments(self, request, queryset):
        updated = queryset.filter(status='confirmed').update(status='completed')
        self.message_user(
            request,
            _('Завершено {} записей').format(updated),
            messages.SUCCESS
        )
    complete_appointments.short_description = _('Завершить выбранные записи')

    def cancel_appointments(self, request, queryset):
        updated = queryset.exclude(status='cancelled').update(status='cancelled')
        self.message_user(
            request,
            _('Отменено {} записей').format(updated),
            messages.SUCCESS
        )
    cancel_appointments.short_description = _('Отменить выбранные записи')

    def mark_as_no_show(self, request, queryset):
        updated = queryset.filter(status='confirmed').update(status='no_show')
        self.message_user(
            request,
            _('Отмечено как неявка {} записей').format(updated),
            messages.SUCCESS
        )
    mark_as_no_show.short_description = _('Отметить как неявка')