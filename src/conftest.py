"""
Root pytest configuration with shared fixtures.
"""

import os

import django
from django.conf import settings

# Устанавливаем настройки Django для pytest
if not settings.configured:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
    django.setup()

import pytest
from django.contrib.auth import get_user_model
from django.test import RequestFactory

User = get_user_model()


@pytest.fixture
def factory():
    return RequestFactory()


@pytest.fixture
def user():
    return User.objects.create_user(username="testuser", email="test@example.com", password="testpass123")


@pytest.fixture
def service_category():
    from apps.services.models import ServiceCategory

    return ServiceCategory.objects.create(name="Диагностика", description="Диагностические услуги")


@pytest.fixture
def service(service_category):
    from apps.services.models import Service

    return Service.objects.create(
        category=service_category,
        name="УЗИ брюшной полости",
        description="Ультразвуковое исследование",
        price=2500.00,
    )


@pytest.fixture
def appointment(user, service):
    import datetime

    from django.utils import timezone

    from apps.appointments.models import Appointment

    return Appointment.objects.create(
        user=user,
        service=service,
        desired_date=timezone.now().date() + datetime.timedelta(days=1),
        desired_time="10:00",
        patient_name="John Doe",
        patient_phone="+1234567890",
        patient_email="john@example.com",
    )
