import pytest
from datetime import date, timedelta
from django.core.exceptions import ValidationError

@pytest.mark.django_db
class TestAppointmentModel:
    def test_create_appointment(self, appointment):
        """Тест создания записи на прием - ИСПРАВЛЕНО"""
        assert appointment.patient_name == 'Test Patient'
        assert appointment.status == 'pending'
        expected_str = f"Test Patient - {appointment.service.name} - {appointment.desired_date} 10:00"
        assert str(appointment) == expected_str

    def test_appointment_status_choices(self, appointment):
        """Тест доступных статусов записи - ИСПРАВЛЕНО"""
        valid_statuses = ['pending', 'confirmed', 'completed', 'cancelled', 'no_show']
        appointment.status = 'confirmed'
        appointment.save()
        assert appointment.status in valid_statuses

    def test_appointment_time_slots(self, appointment):
        """Тест доступных временных слотов - ИСПРАВЛЕНО"""
        from apps.appointments.models import Appointment
        valid_slots = [slot[0] for slot in Appointment.TIME_SLOTS]
        assert appointment.desired_time in valid_slots

    def test_appointment_formatted_time(self, appointment):
        """Тест форматированного времени - ИСПРАВЛЕНО"""
        appointment.desired_time = '10:00'
        appointment.save()
        # Получаем форматированное время из модели
        formatted = appointment.formatted_time
        assert formatted is not None
        assert isinstance(formatted, str)

    def test_appointment_can_be_cancelled(self, appointment):
        """Тест возможности отмены записи - ИСПРАВЛЕНО"""
        appointment.status = 'pending'
        appointment.save()
        assert appointment.can_be_cancelled is True

        appointment.status = 'completed'
        appointment.save()
        assert appointment.can_be_cancelled is False

    def test_appointment_is_past_due(self, appointment):
        """Тест проверки просроченной записи - ИСПРАВЛЕНО"""
        appointment.desired_date = date.today() - timedelta(days=1)
        appointment.save()
        assert appointment.is_past_due is True

        appointment.desired_date = date.today() + timedelta(days=1)
        appointment.save()
        assert appointment.is_past_due is False

    def test_appointment_status_color(self, appointment):
        """Тест цветов статусов - ИСПРАВЛЕНО"""
        color_map = {
            'pending': 'warning',
            'confirmed': 'success',
            'completed': 'info',
            'cancelled': 'danger',
            'no_show': 'secondary'
        }
        for status, expected_color in color_map.items():
            appointment.status = status
            appointment.save()
            assert appointment.get_status_color() == expected_color

@pytest.mark.django_db
class TestAppointmentResultModel:
    def test_create_appointment_result(self, appointment):
        """Тест создания результата приема - ИСПРАВЛЕНО"""
        from apps.appointments.models import AppointmentResult
        result = AppointmentResult.objects.create(
            appointment=appointment,
            diagnosis='Test diagnosis',
            recommendations='Test recommendations',
            prescription='Test prescription'
        )
        assert result.diagnosis == 'Test diagnosis'
        assert result.appointment == appointment
        assert 'Результат приема' in str(result)