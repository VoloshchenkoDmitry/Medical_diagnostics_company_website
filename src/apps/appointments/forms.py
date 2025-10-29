from django import forms
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from .models import Appointment
import datetime


class AppointmentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.service = kwargs.pop('service', None)
        super().__init__(*args, **kwargs)

        # Устанавливаем минимальную дату (завтра)
        tomorrow = timezone.now().date() + datetime.timedelta(days=1)
        self.fields['desired_date'].widget = forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
            'min': tomorrow.isoformat()
        })

        # Настройка виджетов
        self.fields['desired_time'].widget = forms.Select(attrs={'class': 'form-control'})
        self.fields['patient_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['patient_phone'].widget.attrs.update({'class': 'form-control'})
        self.fields['patient_email'].widget.attrs.update({'class': 'form-control'})
        self.fields['patient_age'].widget.attrs.update({'class': 'form-control'})
        self.fields['comments'].widget.attrs.update({
            'class': 'form-control',
            'rows': 4,
            'placeholder': _('Укажите дополнительную информацию, если необходимо')
        })

    class Meta:
        model = Appointment
        fields = [
            'desired_date',
            'desired_time',
            'patient_name',
            'patient_phone',
            'patient_email',
            'patient_age',
            'comments'
        ]
        labels = {
            'desired_date': _('Желаемая дата'),
            'desired_time': _('Желаемое время'),
            'patient_name': _('Имя пациента'),
            'patient_phone': _('Телефон пациента'),
            'patient_email': _('Email пациента'),
            'patient_age': _('Возраст пациента'),
            'comments': _('Комментарий'),
        }

    def clean_desired_date(self):
        desired_date = self.cleaned_data.get('desired_date')
        if desired_date:
            # Проверяем, что дата не в прошлом
            if desired_date < timezone.now().date():
                raise forms.ValidationError(_('Нельзя записаться на прошедшую дату'))

            # Проверяем, что дата не слишком далеко в будущем (максимум 3 месяца)
            max_date = timezone.now().date() + datetime.timedelta(days=90)
            if desired_date > max_date:
                raise forms.ValidationError(_('Запись возможна не более чем на 3 месяца вперед'))

        return desired_date

    def clean(self):
        cleaned_data = super().clean()
        desired_date = cleaned_data.get('desired_date')
        desired_time = cleaned_data.get('desired_time')

        # Проверяем, свободно ли время
        if desired_date and desired_time:
            if Appointment.objects.filter(
                    desired_date=desired_date,
                    desired_time=desired_time,
                    status__in=['pending', 'confirmed']
            ).exists():
                raise forms.ValidationError(
                    _('Выбранное время уже занято. Пожалуйста, выберите другое время.')
                )

        return cleaned_data

    def save(self, commit=True):
        appointment = super().save(commit=False)
        if self.user:
            appointment.user = self.user
        if self.service:
            appointment.service = self.service

        # Заполняем данные пациента из профиля пользователя, если не указаны
        if not appointment.patient_name and self.user:
            appointment.patient_name = self.user.get_full_name() or self.user.username
        if not appointment.patient_email and self.user:
            appointment.patient_email = self.user.email
        if not appointment.patient_phone and self.user.phone:
            appointment.patient_phone = self.user.phone

        if commit:
            appointment.save()

        return appointment


class AppointmentCancelForm(forms.Form):
    reason = forms.CharField(
        label=_('Причина отмены'),
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': _('Укажите причину отмены записи')
        }),
        required=False
    )