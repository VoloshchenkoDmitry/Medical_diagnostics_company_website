from django.test import TestCase
from django.urls import reverse

from apps.services.models import Service, ServiceCategory


class ServicesBasicTests(TestCase):
    """Базовые тесты для приложения services"""

    def setUp(self):
        self.category = ServiceCategory.objects.create(name="Диагностика", description="Диагностические услуги", order=1)
        self.service = Service.objects.create(
            category=self.category,
            name="УЗИ брюшной полости",
            description="Ультразвуковое исследование органов брюшной полости",
            price=2500.00,
            is_active=True,
        )

    def test_service_list_page_status_code(self):
        """Тест страницы списка услуг"""
        response = self.client.get(reverse("services:list"))
        self.assertEqual(response.status_code, 200)

    def test_service_detail_page_status_code(self):
        """Тест страницы деталей услуги"""
        response = self.client.get(reverse("services:detail", args=[self.service.slug]))
        self.assertEqual(response.status_code, 200)

    def test_service_list_template(self):
        """Тест использования правильного шаблона для списка услуг"""
        response = self.client.get(reverse("services:list"))
        self.assertTemplateUsed(response, "services/list.html")

    def test_service_detail_template(self):
        """Тест использования правильного шаблона для деталей услуги"""
        response = self.client.get(reverse("services:detail", args=[self.service.slug]))
        self.assertTemplateUsed(response, "services/detail.html")

    def test_service_creation(self):
        """Тест создания услуги"""
        self.assertEqual(Service.objects.count(), 1)
        self.assertEqual(self.service.name, "УЗИ брюшной полости")
        self.assertEqual(self.service.price, 2500.00)
        self.assertTrue(self.service.is_active)
