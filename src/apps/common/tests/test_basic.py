from django.test import TestCase
from django.urls import reverse


class CommonBasicTests(TestCase):
    """Базовые тесты для приложения common"""

    def test_home_page_status_code(self):
        """Тест главной страницы"""
        response = self.client.get(reverse("common:home"))
        self.assertEqual(response.status_code, 200)

    def test_about_page_status_code(self):
        """Тест страницы 'О компании'"""
        response = self.client.get(reverse("common:about"))
        self.assertEqual(response.status_code, 200)

    def test_contacts_page_status_code(self):
        """Тест страницы контактов"""
        response = self.client.get(reverse("common:contacts"))
        self.assertEqual(response.status_code, 200)

    def test_home_page_template(self):
        """Тест использования правильного шаблона для главной страницы"""
        response = self.client.get(reverse("common:home"))
        self.assertTemplateUsed(response, "common/index.html")

    def test_about_page_template(self):
        """Тест использования правильного шаблона для страницы 'О компании'"""
        response = self.client.get(reverse("common:about"))
        self.assertTemplateUsed(response, "common/about.html")

    def test_contacts_page_template(self):
        """Тест использования правильного шаблона для страницы контактов"""
        response = self.client.get(reverse("common:contacts"))
        self.assertTemplateUsed(response, "common/contacts.html")
