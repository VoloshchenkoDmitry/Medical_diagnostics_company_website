import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
class TestUserModel:
    """Тесты для модели User"""

    def test_create_user(self):
        """Тест создания пользователя"""
        user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )

        assert user.pk is not None
        assert user.username == "testuser"
        assert user.email == "test@example.com"
        assert user.is_active is True
        assert user.is_staff is False
        assert user.is_superuser is False

    def test_create_superuser(self):
        """Тест создания суперпользователя"""
        superuser = User.objects.create_superuser(
            username="admin", email="admin@example.com", password="adminpass123"
        )

        assert superuser.is_staff is True
        assert superuser.is_superuser is True

    def test_user_str_representation(self):
        """Тест строкового представления пользователя"""
        user = User.objects.create_user(username="testuser")
        assert str(user) == "testuser"

    def test_user_get_full_name(self):
        """Тест получения полного имени"""
        user = User.objects.create_user(
            username="testuser", first_name="Иван", last_name="Петров"
        )
        assert user.get_full_name() == "Иван Петров"

    def test_user_get_full_name_without_names(self):
        """Тест получения полного имени когда имя и фамилия не указаны"""
        user = User.objects.create_user(
            username="testuser", first_name="", last_name=""
        )
        assert user.get_full_name() == "testuser"
