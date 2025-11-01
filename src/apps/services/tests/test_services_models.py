import pytest
from django.core.exceptions import ValidationError

from django.db import IntegrityError

from apps.services.models import Service, ServiceCategory


@pytest.mark.django_db
class TestServiceCategoryModel:
    """Тесты для модели ServiceCategory"""

    def test_category_creation_and_str(self):
        """Тест создания категории и строкового представления"""
        category = ServiceCategory.objects.create(
            name="Лабораторная диагностика",
            description="Лабораторные исследования",
            order=1,
        )
        assert category.pk is not None
        assert str(category) == "Лабораторная диагностика"
        assert category.description == "Лабораторные исследования"
        assert category.order == 1

    def test_category_slug_generation(self):
        """Тест что slug генерируется при создании"""
        category = ServiceCategory.objects.create(name="Тестовая Категория")
        # Проверяем что slug создан
        assert category.slug is not None
        assert category.slug != ""
        # Проверяем что slug содержит транслитерированные части
        assert "testovaya" in category.slug
        assert "kategoriya" in category.slug

    def test_category_with_manual_slug(self):
        """Тест категории с ручным slug"""
        category = ServiceCategory.objects.create(name="Категория", slug="manual-slug")
        assert category.slug == "manual-slug"

    def test_category_ordering(self):
        """Тест порядка категорий"""
        cat1 = ServiceCategory.objects.create(name="B", order=2)
        cat2 = ServiceCategory.objects.create(name="A", order=1)
        cat3 = ServiceCategory.objects.create(name="C", order=3)

        categories = ServiceCategory.objects.all()
        assert list(categories) == [cat2, cat1, cat3]


@pytest.mark.django_db
class TestServiceModel:
    """Тесты для модели Service"""

    def test_service_creation_and_str(self):
        """Тест создания услуги и строкового представления"""
        category = ServiceCategory.objects.create(name="Категория")
        service = Service.objects.create(
            category=category,
            name="УЗИ брюшной полости",
            description="Ультразвуковое исследование",
            price=2500.00,
        )
        assert service.pk is not None
        assert str(service) == "УЗИ брюшной полости"
        assert service.price == 2500.00
        assert service.is_active is True

    def test_service_slug_generation(self):
        """Тест что slug генерируется для услуги"""
        category = ServiceCategory.objects.create(name="Категория")
        service = Service.objects.create(
            category=category, name="Тестовая Услуга", price=1000.00
        )
        assert service.slug is not None
        assert service.slug != ""
        assert "testovaya" in service.slug
        assert "usluga" in service.slug

    def test_service_with_manual_slug(self):
        """Тест услуги с ручным slug"""
        category = ServiceCategory.objects.create(name="Категория")
        service = Service.objects.create(
            category=category, name="Услуга", slug="custom-slug", price=1000.00
        )
        assert service.slug == "custom-slug"

    def test_service_price_validation(self):
        """Тест валидации цены"""
        category = ServiceCategory.objects.create(name="Категория")
        service = Service(
            category=category,
            name="Услуга",
            description="Описание услуги",  # Добавляем описание
            price=-100.00,  # Невалидная цена
        )

        with pytest.raises(ValidationError) as exc_info:
            service.full_clean()

        # Проверяем что ошибка связана с полем price
        assert "price" in exc_info.value.error_dict

    def test_service_ordering(self):
        """Тест порядка услуг"""
        category = ServiceCategory.objects.create(name="Категория")
        service1 = Service.objects.create(category=category, name="B", price=1000)
        service2 = Service.objects.create(category=category, name="A", price=2000)
        service3 = Service.objects.create(category=category, name="C", price=3000)

        services = Service.objects.filter(category=category)
        assert list(services) == [service2, service1, service3]

    def test_service_category_relationship(self):
        """Тест связи услуги с категорией"""
        category = ServiceCategory.objects.create(name="Категория")
        service = Service.objects.create(category=category, name="Услуга", price=1000)

        # Проверяем прямую связь
        assert service.category == category
        # Проверяем обратную связь
        assert service in category.services.all()


# Простые smoke-тесты
@pytest.mark.django_db
def test_basic_operations():
    """Базовые операции с моделями"""
    # Создаем категорию
    cat = ServiceCategory.objects.create(name="Тест Категория")
    assert cat.pk is not None

    # Создаем услугу
    service = Service.objects.create(
        category=cat, name="Тест Услуга", description="Описание", price=1000.00
    )
    assert service.pk is not None

    # Проверяем связи
    assert service.category == cat
    assert service in cat.services.all()
