import pytest
from django.contrib.auth import get_user_model
from django.test import Client
from django.urls import reverse

User = get_user_model()


@pytest.mark.django_db
class TestUsersViews:
    """Тесты для views приложения users"""

    def setup_method(self):
        self.client = Client()
        self.user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpass123",
            "first_name": "Тест",
            "last_name": "Пользователь",
        }

    def test_user_register_view_get(self):
        """Тест GET запроса страницы регистрации"""
        response = self.client.get(reverse("users:register"))
        assert response.status_code == 200
        assert (
            "Регистрация - Медицинский Диагностический Центр"
            in response.content.decode()
        )

    def test_user_register_view_post_valid(self):
        """Тест POST запроса с валидными данными регистрации"""
        form_data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password1": "ComplexPass123!",
            "password2": "ComplexPass123!",
            "first_name": "Новый",
            "last_name": "Пользователь",
        }
        response = self.client.post(reverse("users:register"), form_data)

        # После успешной регистрации должен быть редирект
        assert response.status_code == 302
        assert response.url == reverse("users:profile")

        # Проверяем что пользователь создан
        assert User.objects.filter(username="newuser").exists()

    def test_user_login_view_get(self):
        """Тест GET запроса страницы входа"""
        response = self.client.get(reverse("users:login"))
        assert response.status_code == 200
        assert "Вход - Медицинский Диагностический Центр" in response.content.decode()

    def test_user_login_view_post_valid(self):
        """Тест POST запроса с валидными данными входа"""
        user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )

        form_data = {"username": "testuser", "password": "testpass123"}
        response = self.client.post(reverse("users:login"), form_data)

        # После успешного входа должен быть редирект
        assert response.status_code == 302
        assert response.url == reverse("users:profile")

    def test_profile_view_requires_login(self):
        """Тест что профиль требует аутентификации"""
        response = self.client.get(reverse("users:profile"))
        assert response.status_code == 302  # Redirect to login
        assert "login" in response.url

    def test_profile_view_authenticated(self):
        """Тест профиля для аутентифицированного пользователя"""
        user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )
        self.client.login(username="testuser", password="testpass123")

        response = self.client.get(reverse("users:profile"))
        assert response.status_code == 200
        assert (
            "Личный кабинет - Медицинский Диагностический Центр"
            in response.content.decode()
        )
