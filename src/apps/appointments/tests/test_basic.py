import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from apps.appointments.models import Appointment
from apps.services.models import Service, ServiceCategory

User = get_user_model()


class AppointmentsBasicTests(TestCase):
    """Базовые тесты для приложения appointments"""

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", email="test@example.com", password="testpass123")

        self.category = ServiceCategory.objects.create(name="Диагностика", description="Диагностические услуги")

        self.service = Service.objects.create(
            category=self.category,
            name="УЗИ",
            description="Ультразвуковое исследование",
            price=2000.00,
            is_active=True,
        )

        self.appointment_data = {
            "user": self.user,
            "service": self.service,
            "desired_date": timezone.now().date() + datetime.timedelta(days=1),
            "desired_time": "10:00",
            "patient_name": "John Doe",
            "patient_phone": "+1234567890",
            "patient_email": "john@example.com",
            "patient_age": 30,
        }

    def test_appointment_creation(self):
        """Тест создания записи на прием"""
        appointment = Appointment.objects.create(**self.appointment_data)
        self.assertEqual(Appointment.objects.count(), 1)
        self.assertEqual(appointment.patient_name, "John Doe")
        self.assertEqual(appointment.service.name, "УЗИ")
        self.assertEqual(appointment.status, "pending")

    def test_appointment_str_representation(self):
        """Тест строкового представления записи"""
        appointment = Appointment.objects.create(**self.appointment_data)
        expected_str = (
            f"{appointment.patient_name} - {appointment.service.name} - {appointment.desired_date} {appointment.desired_time}"
        )
        self.assertEqual(str(appointment), expected_str)

    def test_appointment_formatted_time(self):
        """Тест форматированного времени"""
        appointment = Appointment.objects.create(**self.appointment_data)
        self.assertEqual(appointment.formatted_time, "10:00 - 10:30")
