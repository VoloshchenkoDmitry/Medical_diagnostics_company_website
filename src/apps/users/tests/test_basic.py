from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

User = get_user_model()


class UsersBasicTests(TestCase):
    """Базовые тесты для приложения users"""

    def setUp(self):
        self.user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpass123",
            "first_name": "John",
            "last_name": "Doe",
        }

    def test_register_page_status_code(self):
        """Тест страницы регистрации"""
        response = self.client.get(reverse("users:register"))
        self.assertEqual(response.status_code, 200)

    def test_login_page_status_code(self):
        """Тест страницы входа"""
        response = self.client.get(reverse("users:login"))
        self.assertEqual(response.status_code, 200)

    def test_register_page_template(self):
        """Тест использования правильного шаблона для регистрации"""
        response = self.client.get(reverse("users:register"))
        self.assertTemplateUsed(response, "users/register.html")

    def test_login_page_template(self):
        """Тест использования правильного шаблона для входа"""
        response = self.client.get(reverse("users:login"))
        self.assertTemplateUsed(response, "users/login.html")

    def test_user_creation(self):
        """Тест создания пользователя"""
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.email, "test@example.com")
        self.assertTrue(user.check_password("testpass123"))
