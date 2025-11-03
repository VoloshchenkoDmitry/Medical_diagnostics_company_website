"""
Pytest configuration for services app tests.
"""
import pytest


@pytest.fixture
def service_category_data():
    """Service category test data."""
    return {
        "name": "Диагностика",
        "description": "Диагностические услуги",
        "order": 1,
    }


@pytest.fixture
def test_category(db, service_category_data):
    """Create a test service category."""
    from apps.services.models import ServiceCategory

    # Создаем категорию напрямую - slug сгенерируется автоматически
    category = ServiceCategory.objects.create(**service_category_data)
    return category


@pytest.fixture
def service_data(test_category):
    """Service test data."""
    return {
        "category": test_category,
        "name": "УЗИ брюшной полости",
        "description": "Ультразвуковое исследование органов брюшной полости",
        "price": 2500.00,
        "is_active": True,
    }


@pytest.fixture
def test_service(db, service_data):
    """Create a test service."""
    from apps.services.models import Service

    # Создаем услугу напрямую - slug сгенерируется автоматически
    service = Service.objects.create(**service_data)
    return service


@pytest.fixture
def another_category(db):
    """Create another test service category."""
    from apps.services.models import ServiceCategory

    # Создаем другую категорию с уникальным именем
    category = ServiceCategory.objects.create(name="Анализы", description="Лабораторные анализы", order=2)
    return category
