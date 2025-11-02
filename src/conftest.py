import pytest
from django.test import RequestFactory
from apps.users.models import User

@pytest.fixture
def user():
    """Создает тестового пользователя"""
    return User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123',
        first_name='Test',
        last_name='User'
    )

@pytest.fixture
def admin_user():
    """Создает тестового администратора"""
    return User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='adminpass123'
    )

@pytest.fixture
def rf():
    """Request factory fixture"""
    return RequestFactory()

@pytest.fixture
def authenticated_client(client, user):
    """Клиент с аутентифицированным пользователем"""
    client.force_login(user)
    return client

@pytest.fixture
def strong_password():
    """Возвращает надежный пароль для тестов"""
    return 'TestPassword123!'