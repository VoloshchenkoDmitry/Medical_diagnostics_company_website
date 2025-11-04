from django.test import TestCase
from django.urls import resolve, reverse

from apps.common import views


class CommonURLTests(TestCase):
    """Тесты URL для приложения common"""

    def test_home_url_resolves(self):
        """Тест разрешения URL для главной страницы"""
        url = reverse("common:home")
        self.assertEqual(resolve(url).func.view_class, views.HomeView)

    def test_about_url_resolves(self):
        """Тест разрешения URL для страницы 'О компании'"""
        url = reverse("common:about")
        self.assertEqual(resolve(url).func.view_class, views.AboutView)

    def test_contacts_url_resolves(self):
        """Тест разрешения URL для страницы контактов"""
        url = reverse("common:contacts")
        self.assertEqual(resolve(url).func.view_class, views.ContactsView)
