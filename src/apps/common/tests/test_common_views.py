import pytest
from django.test import Client
from django.urls import reverse


@pytest.mark.django_db
class TestCommonViews:
    """Тесты для views приложения common"""

    def setup_method(self):
        self.client = Client()

    def test_home_view(self):
        """Тест главной страницы"""
        response = self.client.get(reverse("common:home"))
        assert response.status_code == 200
        assert "Медицинский Диагностический Центр" in response.content.decode()

    def test_about_view(self):
        """Тест страницы 'О компании'"""
        response = self.client.get(reverse("common:about"))
        assert response.status_code == 200
        assert "О компании" in response.content.decode()

    def test_contacts_view_get(self):
        """Тест GET запроса страницы контактов"""
        response = self.client.get(reverse("common:contacts"))
        assert response.status_code == 200
        assert "Контакты" in response.content.decode()
        assert "form" in response.content.decode()
