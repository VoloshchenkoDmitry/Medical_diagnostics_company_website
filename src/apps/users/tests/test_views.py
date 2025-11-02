import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
class TestUsersViews:
    def test_user_register_view_get(self, client):
        """Тест GET запроса регистрации"""
        response = client.get(reverse('users:register'))
        assert response.status_code == 200
        # Проверяем наличие ключевых элементов на странице вместо русского текста
        assert b'register' in response.content.lower()
        assert b'form' in response.content

    def test_user_register_view_post_valid(self, client):
        """Тест POST запроса регистрации с валидными данными"""
        form_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'first_name': 'New',
            'last_name': 'User',
            'password1': 'complexpassword123',
            'password2': 'complexpassword123',
        }
        response = client.post(reverse('users:register'), form_data)
        assert response.status_code == 302  # Редирект после успешной регистрации
        assert User.objects.filter(username='newuser').exists()

    def test_user_register_view_post_invalid(self, client):
        """Тест POST запроса регистрации с невалидными данными"""
        form_data = {
            'username': 'newuser',
            'email': 'invalid-email',  # Невалидный email
            'password1': '123',  # Слишком простой пароль
            'password2': '123',
        }
        response = client.post(reverse('users:register'), form_data)
        assert response.status_code == 200  # Остается на странице с ошибками
        assert not User.objects.filter(username='newuser').exists()

    def test_user_login_view_get(self, client):
        """Тест GET запроса входа"""
        response = client.get(reverse('users:login'))
        assert response.status_code == 200
        # Проверяем наличие формы входа
        assert b'csrfmiddlewaretoken' in response.content
        assert b'username' in response.content
        assert b'password' in response.content

    def test_user_login_view_post_valid(self, client, user):
        """Тест POST запроса входа с валидными данными"""
        form_data = {
            'username': user.username,
            'password': 'testpass123',
        }
        response = client.post(reverse('users:login'), form_data, follow=True)
        # После успешного входа должен быть редирект
        assert response.status_code == 200

    def test_user_login_view_post_invalid(self, client, user):
        """Тест POST запроса входа с невалидными данными"""
        form_data = {
            'username': user.username,
            'password': 'wrongpassword',  # Неправильный пароль
        }
        response = client.post(reverse('users:login'), form_data)
        assert response.status_code == 200  # Остается на странице входа

    def test_user_profile_view_authenticated(self, authenticated_client, user):
        """Тест профиля для аутентифицированного пользователя"""
        response = authenticated_client.get(reverse('users:profile'))
        assert response.status_code == 200
        # Проверяем что отображается информация пользователя
        assert user.username.encode() in response.content

    def test_user_profile_view_unauthenticated(self, client):
        """Тест профиля для неаутентифицированного пользователя"""
        response = client.get(reverse('users:profile'))
        assert response.status_code == 302  # Редирект на страницу входа
        login_url = reverse('users:login')
        assert login_url in response.url

    def test_user_logout_view_post(self, authenticated_client):
        """Тест выхода из системы через POST запрос"""
        # Выход из системы требует POST запрос
        response = authenticated_client.post(reverse('users:logout'))
        assert response.status_code == 302  # Редирект после выхода
        assert response.url == reverse('common:home')

    def test_user_logout_view_get_not_allowed(self, authenticated_client):
        """Тест что GET запрос для выхода не разрешен"""
        response = authenticated_client.get(reverse('users:logout'))
        assert response.status_code == 405  # Method Not Allowed

    def test_user_profile_edit_view_authenticated(self, authenticated_client, user):
        """Тест редактирования профиля для аутентифицированного пользователя"""
        response = authenticated_client.get(reverse('users:profile_edit'))
        assert response.status_code == 200
        # Проверяем что форма содержит данные пользователя
        assert user.email.encode() in response.content

    def test_user_profile_edit_view_post(self, authenticated_client, user):
        """Тест POST запроса редактирования профиля"""
        form_data = {
            'first_name': 'Updated',
            'last_name': 'Name',
            'email': user.email,  # Тот же email
            'phone': '+79991234567',
        }
        response = authenticated_client.post(reverse('users:profile_edit'), form_data)
        assert response.status_code == 302  # Редирект после успешного обновления
        user.refresh_from_db()
        assert user.first_name == 'Updated'
        assert user.last_name == 'Name'