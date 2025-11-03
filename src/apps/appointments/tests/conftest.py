import datetime

import pytest
from django.contrib.auth import get_user_model
from django.utils import timezone

from apps.appointments.models import Appointment, AppointmentResult
from apps.services.models import Service, ServiceCategory

User = get_user_model()


@pytest.fixture
def test_user(db):
    """Создает тестового пользователя"""
    return User.objects.create_user(username="testuser", email="test@example.com", password="testpass123")


@pytest.fixture
def test_category(db):
    """Создает тестовую категорию услуг"""
    return ServiceCategory.objects.create(name="Диагностика", description="Диагностические услуги")


@pytest.fixture
def test_service(db, test_category):
    """Создает тестовую услугу"""
    return Service.objects.create(
        category=test_category,
        name="УЗИ брюшной полости",
        description="Ультразвуковое исследование органов брюшной полости",
        price=2500.00,
    )


@pytest.fixture
def appointment_data(test_user, test_service):
    """Данные для создания записи на прием"""
    tomorrow = timezone.now().date() + datetime.timedelta(days=1)
    return {
        "user": test_user,
        "service": test_service,
        "desired_date": tomorrow,
        "desired_time": "10:00",
        "patient_name": "John Doe",
        "patient_phone": "+1234567890",
        "patient_email": "john@example.com",
        "patient_age": 30,
    }


@pytest.fixture
def test_appointment(db, appointment_data):
    """Создает тестовую запись на прием"""
    return Appointment.objects.create(**appointment_data)


@pytest.fixture
def appointment_result_data(test_appointment):
    """Данные для создания результата приема"""
    return {
        "appointment": test_appointment,
        "diagnosis": "Здоров",
        "recommendations": "Регулярные обследования",
        "prescription": "Витамины",
    }


@pytest.fixture
def test_appointment_result(db, appointment_result_data):
    """Создает тестовый результат приема"""
    return AppointmentResult.objects.create(**appointment_result_data)
