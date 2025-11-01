from datetime import date, timedelta

import pytest
from django.utils import timezone

from apps.appointments.models import Appointment
from apps.services.models import Service, ServiceCategory
from apps.users.models import User


@pytest.mark.django_db
class TestAppointmentModel:
    """Тесты для модели Appointment"""

    def test_create_appointment(self):
        """Тест создания записи на прием"""
        # Создаем тестовые данные
        user = User.objects.create_user(username="testuser", email="test@example.com")
        category = ServiceCategory.objects.create(name="Категория", slug="category")
        service = Service.objects.create(
            category=category, name="Услуга", slug="service", price=1000.00
        )

        appointment = Appointment.objects.create(
            user=user,
            service=service,
            desired_date=date.today() + timedelta(days=1),
            desired_time="10:00",
            patient_name="Иван Иванов",
            patient_phone="+79991234567",
            patient_email="patient@example.com",
        )

        assert appointment.pk is not None
        assert appointment.status == "pending"
        assert appointment.patient_name == "Иван Иванов"

    def test_appointment_str_representation(self):
        """Тест строкового представления записи"""
        user = User.objects.create_user(username="testuser")
        category = ServiceCategory.objects.create(name="Категория", slug="category")
        service = Service.objects.create(
            category=category, name="УЗИ", price=1000, slug="uzi"
        )

        appointment = Appointment.objects.create(
            user=user,
            service=service,
            desired_date=date(2024, 1, 15),
            desired_time="10:00",
            patient_name="Иван Иванов",
            patient_phone="+79991234567",
        )

        expected_str = "Иван Иванов - УЗИ - 2024-01-15 10:00"
        assert str(appointment) == expected_str

    def test_appointment_status_color(self):
        """Тест цвета статуса"""
        user = User.objects.create_user(username="testuser")
        category = ServiceCategory.objects.create(name="Категория", slug="category")
        service = Service.objects.create(
            category=category, name="Услуга", price=1000, slug="service"
        )

        appointment = Appointment.objects.create(
            user=user,
            service=service,
            desired_date=date.today() + timedelta(days=1),
            desired_time="10:00",
            patient_name="Тест",
            patient_phone="+79991234567",
        )

        appointment.status = "pending"
        assert appointment.get_status_color() == "warning"

        appointment.status = "confirmed"
        assert appointment.get_status_color() == "success"

        appointment.status = "completed"
        assert appointment.get_status_color() == "info"

        appointment.status = "cancelled"
        assert appointment.get_status_color() == "danger"

    def test_appointment_is_past_due(self):
        """Тест проверки просроченной записи"""
        user = User.objects.create_user(username="testuser")
        category = ServiceCategory.objects.create(name="Категория", slug="category")
        service = Service.objects.create(
            category=category, name="Услуга", price=1000, slug="service"
        )

        # Прошедшая дата
        past_date = timezone.now().date() - timedelta(days=1)
        appointment = Appointment.objects.create(
            user=user,
            service=service,
            desired_date=past_date,
            desired_time="10:00",
            patient_name="Тест",
            patient_phone="+79991234567",
        )
        assert appointment.is_past_due is True

        # Будущая дата
        future_date = timezone.now().date() + timedelta(days=1)
        appointment_future = Appointment.objects.create(
            user=user,
            service=service,
            desired_date=future_date,
            desired_time="10:00",
            patient_name="Тест2",
            patient_phone="+79991234568",
        )
        assert appointment_future.is_past_due is False
