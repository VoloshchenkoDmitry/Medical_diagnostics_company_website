import pytest
from django.db import IntegrityError
from django.test import TestCase

from apps.services.models import Service, ServiceCategory


class ServiceCategoryModelTest(TestCase):
    def setUp(self):
        self.category_data = {
            "name": "Диагностика",
            "description": "Диагностические услуги",
            "order": 1,
        }

    def test_create_service_category(self):
        """Test creating a service category"""
        category = ServiceCategory.objects.create(**self.category_data)

        self.assertEqual(category.name, "Диагностика")
        self.assertEqual(category.description, "Диагностические услуги")
        self.assertEqual(category.order, 1)
        self.assertEqual(category.slug, "diagnostika")
        self.assertIsNotNone(category.created_at)

    def test_service_category_str_representation(self):
        """Test string representation of service category"""
        category = ServiceCategory.objects.create(**self.category_data)
        self.assertEqual(str(category), "Диагностика")

    def test_service_category_ordering(self):
        """Test that categories are ordered by order and name"""
        category1 = ServiceCategory.objects.create(name="Б", order=2)
        category2 = ServiceCategory.objects.create(name="А", order=1)

        categories = ServiceCategory.objects.all()
        self.assertEqual(categories[0], category2)  # Lower order first
        self.assertEqual(categories[1], category1)

    def test_service_category_slug_generation(self):
        """Test automatic slug generation for category"""
        category = ServiceCategory.objects.create(name="Новая категория")
        self.assertEqual(category.slug, "novaya-kategoriya")

    def test_service_category_unique_slug(self):
        """Test that slug is unique for categories"""
        category1 = ServiceCategory.objects.create(name="Тест")
        category2 = ServiceCategory.objects.create(name="Тест")  # Должен получить уникальный slug

        self.assertEqual(category1.slug, "test")
        self.assertNotEqual(category2.slug, "test")  # Должен быть другим
        self.assertTrue(category2.slug.startswith("test-"))

    def test_service_category_slug_with_special_chars(self):
        """Test slug generation with special characters"""
        category = ServiceCategory.objects.create(name="Категория с цифрами 123!")
        # Специальные символы должны быть удалены, "ц" транслитерируется как "c"
        self.assertEqual(category.slug, "kategoriya-s-ciframi-123")


class ServiceModelTest(TestCase):
    def setUp(self):
        self.category = ServiceCategory.objects.create(name="Диагностика", description="Диагностические услуги")

        self.service_data = {
            "category": self.category,
            "name": "УЗИ брюшной полости",
            "description": "Ультразвуковое исследование органов брюшной полости",
            "price": 2500.00,
            "is_active": True,
        }

    def test_create_service(self):
        """Test creating a service"""
        service = Service.objects.create(**self.service_data)

        self.assertEqual(service.name, "УЗИ брюшной полости")
        self.assertEqual(service.category, self.category)
        self.assertEqual(service.price, 2500.00)
        self.assertTrue(service.is_active)
        self.assertEqual(service.slug, "uzi-bryushnoy-polosti")
        self.assertIsNotNone(service.created_at)

    def test_service_str_representation(self):
        """Test string representation of service"""
        service = Service.objects.create(**self.service_data)
        self.assertEqual(str(service), "УЗИ брюшной полости")

    def test_service_slug_auto_generation(self):
        """Test automatic slug generation"""
        service = Service.objects.create(**self.service_data)
        expected_slug = "uzi-bryushnoy-polosti"
        self.assertEqual(service.slug, expected_slug)

    def test_service_ordering(self):
        """Test that services are ordered by category and name"""
        category2 = ServiceCategory.objects.create(name="Анализы")

        service1 = Service.objects.create(category=self.category, name="Б-Услуга", description="Test", price=1000)
        service2 = Service.objects.create(category=self.category, name="А-Услуга", description="Test", price=1000)
        service3 = Service.objects.create(category=category2, name="Анализ крови", description="Test", price=1000)

        services = Service.objects.all()
        self.assertEqual(services[0], service3)  # Different category
        self.assertEqual(services[1], service2)  # Same category, alphabetically first
        self.assertEqual(services[2], service1)

    def test_service_save_updates_slug(self):
        """Test that slug is updated when name changes"""
        service = Service.objects.create(
            category=self.category,
            name="Старое название",
            description="Test",
            price=1000,
        )
        original_slug = service.slug
        self.assertEqual(original_slug, "staroe-nazvanie")  # Проверяем исходный slug

        service.name = "Новое название услуги"
        service.save()

        # Должен быть новый slug
        self.assertNotEqual(service.slug, original_slug)
        self.assertEqual(service.slug, "novoe-nazvanie-uslugi")

    def test_service_unique_slug_constraint(self):
        """Test that services cannot have duplicate slugs"""
        service1 = Service.objects.create(
            category=self.category,
            name="Уникальная услуга",
            description="Test",
            price=1000,
        )

        # Попытка создать услугу с тем же именем должна создать уникальный slug
        service2 = Service.objects.create(
            category=self.category,
            name="Уникальная услуга",
            description="Test",
            price=1000,
        )

        self.assertEqual(service1.slug, "unikalnaya-usluga")
        self.assertNotEqual(service2.slug, "unikalnaya-usluga")
        self.assertTrue(service2.slug.startswith("unikalnaya-usluga-"))

    def test_service_slug_with_special_chars(self):
        """Test slug generation with special characters"""
        service = Service.objects.create(
            category=self.category,
            name="Услуга с цифрами 123!",
            description="Test",
            price=1000,
        )
        # Специальные символы должны быть удалены, "ц" транслитерируется как "c"
        self.assertEqual(service.slug, "usluga-s-ciframi-123")

    def test_service_slug_cyrillic_transliteration(self):
        """Test cyrillic transliteration in slug generation"""
        service = Service.objects.create(
            category=self.category,
            name="Магнитно-резонансная томография",
            description="Test",
            price=1000,
        )
        # Дефисы должны сохраняться
        self.assertEqual(service.slug, "magnitno-rezonansnaya-tomografiya")

    def test_service_slug_no_change_when_name_unchanged(self):
        """Test that slug doesn't change when name remains the same"""
        service = Service.objects.create(
            category=self.category,
            name="Постоянное название",
            description="Test",
            price=1000,
        )
        original_slug = service.slug

        # Изменяем другое поле
        service.price = 2000
        service.save()

        # Slug должен остаться прежним
        self.assertEqual(service.slug, original_slug)
