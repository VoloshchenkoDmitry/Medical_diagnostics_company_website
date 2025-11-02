import pytest
from datetime import date, timedelta
from apps.appointments.models import Appointment, AppointmentResult
from apps.services.models import Service, ServiceCategory
from apps.users.models import User

@pytest.fixture
def appointment_user():
    """Создает пользователя для тестов записей"""
    return User.objects.create_user(
        username='appointmentuser',
        email='appointment@example.com',
        password='testpass123'
    )

@pytest.fixture
def appointment_category():
    """Создает категорию для тестов записей"""
    return ServiceCategory.objects.create(
        name='Тестовая категория записей',
        description='Описание',
        order=1
    )

@pytest.fixture
def appointment_service(appointment_category):
    """Создает услугу для тестов записей"""
    return Service.objects.create(
        category=appointment_category,
        name='Тестовая услуга записи',
        description='Описание тестовой услуги',
        price=1000.00,
        is_active=True
    )

@pytest.fixture
def appointment(appointment_user, appointment_service):
    """Создает тестовую запись на прием"""
    return Appointment.objects.create(
        user=appointment_user,
        service=appointment_service,
        desired_date=date.today() + timedelta(days=1),
        desired_time='10:00',
        patient_name='Test Patient',
        patient_phone='+79991234567',
        patient_email='patient@example.com',
        status='pending'
    )