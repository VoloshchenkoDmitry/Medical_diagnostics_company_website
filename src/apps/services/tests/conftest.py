# src/apps/services/tests/conftest.py
import pytest

from apps.services.models import Service, ServiceCategory


@pytest.fixture
def service_category():
    """Фикстура для тестовой категории услуг"""
    return ServiceCategory.objects.create(
        name="Тестовая категория", description="Описание тестовой категории", order=1
    )


@pytest.fixture
def service(service_category):
    """Фикстура для тестовой услуги"""
    return Service.objects.create(
        category=service_category,
        name="Тестовая услуга",
        description="Описание тестовой услуги",
        price=1000.00,
    )


@pytest.fixture
def multiple_categories():
    """Фикстура для нескольких категорий"""
    cat1 = ServiceCategory.objects.create(name="Категория A", order=2)
    cat2 = ServiceCategory.objects.create(name="Категория B", order=1)
    cat3 = ServiceCategory.objects.create(name="Категория C", order=3)
    return [cat1, cat2, cat3]


@pytest.fixture
def multiple_services(service_category):
    """Фикстура для нескольких услуг"""
    service1 = Service.objects.create(
        category=service_category,
        name="Услуга A",
        description="Описание A",
        price=1000.00,
    )
    service2 = Service.objects.create(
        category=service_category,
        name="Услуга B",
        description="Описание B",
        price=2000.00,
    )
    service3 = Service.objects.create(
        category=service_category,
        name="Услуга C",
        description="Описание C",
        price=3000.00,
    )
    return [service1, service2, service3]
