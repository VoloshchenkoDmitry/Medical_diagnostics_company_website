import pytest
from django.core.exceptions import ValidationError
from apps.users.models import User

@pytest.mark.django_db
class TestUserModel:
    def test_create_user(self):
        """Тест создания обычного пользователя"""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User',
            phone='+79991234567'
        )
        assert user.username == 'testuser'
        assert user.email == 'test@example.com'
        assert user.check_password('testpass123')
        assert user.is_active is True
        assert user.is_staff is False
        assert user.is_superuser is False

    def test_create_superuser(self):
        """Тест создания суперпользователя"""
        admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpass123'
        )
        assert admin_user.is_staff is True
        assert admin_user.is_superuser is True

    def test_user_str_representation(self, user):
        """Тест строкового представления пользователя"""
        assert str(user) == user.username

    def test_user_full_name(self, user):
        """Тест полного имени пользователя"""
        user.first_name = 'John'
        user.last_name = 'Doe'
        assert user.get_full_name() == 'John Doe'

    def test_user_full_name_empty(self, user):
        """Тест полного имени когда имя и фамилия пустые"""
        user.first_name = ''
        user.last_name = ''
        assert user.get_full_name() == user.username

    def test_user_unique_email(self, user):
        """Тест уникальности email"""
        with pytest.raises(Exception):  # Должно вызвать исключение при дубликате email
            User.objects.create_user(
                username='anotheruser',
                email=user.email,  # Тот же email
                password='testpass123'
            )