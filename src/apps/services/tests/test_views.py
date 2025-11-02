import pytest
from django.urls import reverse

@pytest.mark.django_db
class TestServicesViews:
    def test_service_list_view(self, client, service):
        """Тест списка услуг"""
        response = client.get(reverse('services:list'))
        assert response.status_code == 200
        assert 'text/html' in response['Content-Type']

    def test_service_list_view_with_category(self, client, service_category, service):
        """Тест списка услуг с фильтрацией по категории"""
        url = f"{reverse('services:list')}?category={service_category.id}"
        response = client.get(url)
        assert response.status_code == 200
        assert 'text/html' in response['Content-Type']

    def test_service_detail_view(self, client, service):
        """Тест детальной страницы услуги"""
        response = client.get(reverse('services:detail', args=[service.slug]))
        assert response.status_code == 200
        assert 'text/html' in response['Content-Type']

    def test_service_detail_view_not_found(self, client):
        """Тест несуществующей услуги"""
        response = client.get(reverse('services:detail', args=['non-existent-slug']))
        assert response.status_code == 404

    def test_service_list_view_empty(self, client):
        """Тест пустого списка услуг"""
        response = client.get(reverse('services:list'))
        assert response.status_code == 200
        assert 'text/html' in response['Content-Type']