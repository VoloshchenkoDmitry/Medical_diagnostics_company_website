import pytest
from apps.services.models import Service, ServiceCategory

@pytest.fixture
def service_category():
    """Создает тестовую категорию услуг"""
    return ServiceCategory.objects.create(
        name='Тестовая категория',
        description='Описание тестовой категории',
        order=1
    )

@pytest.fixture
def service(service_category):
    """Создает тестовую услугу"""
    return Service.objects.create(
        category=service_category,
        name='Тестовая услуга',
        slug='testovaya-usluga',
        description='Описание тестовой услуги',
        price=1000.00,
        is_active=True
    )