import pytest
from django.test import Client
from django.urls import reverse

from apps.services.models import Service, ServiceCategory


@pytest.mark.django_db
class TestServicesViews:
    """Тесты для views приложения services"""

    def setup_method(self):
        self.client = Client()

    def test_service_list_view(self):
        """Тест списка услуг"""
        # Создаем тестовые данные
        category = ServiceCategory.objects.create(
            name="Тестовая категория", slug="test-category"
        )
        Service.objects.create(
            category=category,
            name="Тестовая услуга",
            slug="test-service",
            description="Описание тестовой услуги",
            price=1000.00,
        )

        response = self.client.get(reverse("services:list"))
        assert response.status_code == 200
        assert "Услуги - Медицинский Диагностический Центр" in response.content.decode()
        assert "Тестовая услуга" in response.content.decode()

    def test_service_list_view_with_category_filter(self):
        """Тест фильтрации услуг по категории"""
        category1 = ServiceCategory.objects.create(name="Категория 1", slug="cat1")
        category2 = ServiceCategory.objects.create(name="Категория 2", slug="cat2")

        Service.objects.create(
            category=category1,
            name="Услуга 1",
            slug="service1",
            description="Описание 1",
            price=1000.00,
        )
        Service.objects.create(
            category=category2,
            name="Услуга 2",
            slug="service2",
            description="Описание 2",
            price=2000.00,
        )

        response = self.client.get(
            f"{reverse('services:list')}?category={category1.id}"
        )
        assert response.status_code == 200
        assert "Услуга 1" in response.content.decode()
        assert "Услуга 2" not in response.content.decode()

    def test_service_detail_view(self):
        """Тест детальной страницы услуги"""
        category = ServiceCategory.objects.create(name="Категория", slug="category")
        service = Service.objects.create(
            category=category,
            name="Детальная услуга",
            slug="detail-service",
            description="Подробное описание услуги",
            price=1500.00,
        )

        response = self.client.get(
            reverse("services:detail", kwargs={"service_slug": service.slug})
        )
        assert response.status_code == 200
        assert (
            "Детальная услуга - Медицинский Диагностический Центр"
            in response.content.decode()
        )
        assert "1500" in response.content.decode()

    def test_service_detail_view_not_found(self):
        """Тест несуществующей услуги"""
        response = self.client.get(
            reverse("services:detail", kwargs={"service_slug": "non-existent"})
        )
        assert response.status_code == 404
