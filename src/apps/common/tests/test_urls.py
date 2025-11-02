import pytest
from django.urls import reverse, resolve
from apps.common import views

@pytest.mark.django_db
class TestCommonURLs:
    def test_home_url(self):
        """Тест URL главной страницы"""
        path = reverse('common:home')
        assert path == '/'
        assert resolve(path).func.view_class == views.HomeView

    def test_about_url(self):
        """Тест URL страницы 'О компании'"""
        path = reverse('common:about')
        assert path == '/about/'
        assert resolve(path).func.view_class == views.AboutView

    def test_contacts_url(self):
        """Тест URL страницы контактов"""
        path = reverse('common:contacts')
        assert path == '/contacts/'
        assert resolve(path).func.view_class == views.ContactsView