from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = [
        'username',
        'email',
        'first_name',
        'last_name',
        'phone',
        'is_staff',
        'is_active',
        'date_joined',
        'appointment_count'
    ]
    list_filter = [
        'is_staff',
        'is_active',
        'is_superuser',
        'gender',
        'date_joined',
        'last_login'
    ]
    search_fields = [
        'username',
        'email',
        'first_name',
        'last_name',
        'phone'
    ]
    readonly_fields = [
        'date_joined',
        'last_login',
        'created_at',
        'updated_at',
        'avatar_preview'
    ]
    ordering = ['-date_joined']

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Персональная информация'), {
            'fields': (
                'first_name',
                'last_name',
                'email',
                'phone',
                'date_of_birth',
                'gender',
                'address'
            )
        }),
        (_('Аватар'), {
            'fields': (
                'avatar',
                'avatar_preview'
            )
        }),
        (_('Права доступа'), {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions'
            ),
        }),
        (_('Важные даты'), {
            'fields': (
                'last_login',
                'date_joined',
                'created_at',
                'updated_at'
            ),
            'classes': ('collapse',)
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username',
                'email',
                'password1',
                'password2',
                'first_name',
                'last_name',
                'phone'
            ),
        }),
    )

    def avatar_preview(self, obj):
        if obj.avatar:
            return format_html(
                '<img src="{}" width="100" height="100" style="object-fit: cover; border-radius: 8px;" />',
                obj.avatar.url
            )
        return _("Аватар не загружен")

    avatar_preview.short_description = _('Предпросмотр аватара')

    def appointment_count(self, obj):
        return obj.appointments.count()

    appointment_count.short_description = _('Записей')

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('appointments')

    # Действия в админке
    actions = ['activate_users', 'deactivate_users', 'make_staff', 'remove_staff']

    def activate_users(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(
            request,
            _('Активировано {} пользователей').format(updated),
            messages.SUCCESS
        )

    activate_users.short_description = _('Активировать выбранных пользователей')

    def deactivate_users(self, request, queryset):
        # Нельзя деактивировать себя
        if request.user in queryset:
            self.message_user(
                request,
                _('Вы не можете деактивировать свой собственный аккаунт'),
                messages.ERROR
            )
            queryset = queryset.exclude(pk=request.user.pk)

        updated = queryset.update(is_active=False)
        if updated > 0:
            self.message_user(
                request,
                _('Деактивировано {} пользователей').format(updated),
                messages.SUCCESS
            )

    deactivate_users.short_description = _('Деактивировать выбранных пользователей')

    def make_staff(self, request, queryset):
        updated = queryset.update(is_staff=True)
        self.message_user(
            request,
            _('Назначено персоналом {} пользователей').format(updated),
            messages.SUCCESS
        )

    make_staff.short_description = _('Назначить персоналом')

    def remove_staff(self, request, queryset):
        # Нельзя удалить права персонала у себя
        if request.user in queryset:
            self.message_user(
                request,
                _('Вы не можете удалить права персонала у себя'),
                messages.ERROR
            )
            queryset = queryset.exclude(pk=request.user.pk)

        updated = queryset.update(is_staff=False)
        if updated > 0:
            self.message_user(
                request,
                _('Убраны права персонала у {} пользователей').format(updated),
                messages.SUCCESS
            )

    remove_staff.short_description = _('Убрать права персонала')