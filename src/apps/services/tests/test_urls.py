from django.test import TestCase
from django.urls import resolve, reverse

from apps.services import views


class ServicesURLTests(TestCase):
    """Тесты URL для приложения services"""

    def test_service_list_url_resolves(self):
        """Тест разрешения URL для списка услуг"""
        url = reverse("services:list")
        self.assertEqual(resolve(url).func.view_class, views.ServiceListView)

    def test_service_detail_url_resolves(self):
        """Тест разрешения URL для деталей услуги"""
        url = reverse("services:detail", args=["test-service"])
        self.assertEqual(resolve(url).func.view_class, views.ServiceDetailView)
