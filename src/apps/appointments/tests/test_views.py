import pytest
from datetime import date, timedelta
from django.urls import reverse


@pytest.mark.django_db
class TestAppointmentsViews:
    def test_appointment_list_view_authenticated(self, authenticated_client, appointment):
        """Тест списка записей для аутентифицированного пользователя"""
        response = authenticated_client.get(reverse('appointments:list'))
        assert response.status_code == 200
        assert 'text/html' in response['Content-Type']

    def test_appointment_list_view_unauthenticated(self, client):
        """Тест списка записей для неаутентифицированного пользователя"""
        response = client.get(reverse('appointments:list'))
        assert response.status_code == 302  # Редирект на страницу входа
        assert reverse('users:login') in response.url

    def test_appointment_create_view_authenticated(self, authenticated_client, appointment_service):
        """Тест создания записи для аутентифицированного пользователя"""
        response = authenticated_client.get(reverse('appointments:create', args=[appointment_service.slug]))
        assert response.status_code == 200
        assert 'text/html' in response['Content-Type']

    def test_appointment_create_view_post_valid(self, authenticated_client, appointment_service, user):
        """Тест POST запроса создания записи с валидными данными"""
        form_data = {
            'desired_date': str(date.today() + timedelta(days=1)),
            'desired_time': '10:00',
            'patient_name': user.get_full_name() or user.username,
            'patient_phone': '+79991234567',
            'patient_email': user.email,
            'patient_age': 30,
            'comments': 'Test comments'
        }
        response = authenticated_client.post(
            reverse('appointments:create', args=[appointment_service.slug]),
            form_data
        )
        # После создания должен быть редирект или успешный ответ
        assert response.status_code in [200, 302]

    def test_appointment_detail_view_authenticated(self, authenticated_client, appointment, user):
        """Тест детальной страницы записи для владельца - ИСПРАВЛЕНО"""
        # Убедимся что пользователь является владельцем записи
        appointment.user = user
        appointment.save()

        response = authenticated_client.get(reverse('appointments:detail', args=[appointment.pk]))
        assert response.status_code == 200
        assert 'text/html' in response['Content-Type']

    def test_appointment_detail_view_other_user(self, client, appointment, appointment_user):
        """Тест детальной страницы записи для другого пользователя"""
        # Создаем другого пользователя
        from apps.users.models import User
        other_user = User.objects.create_user(
            username='otheruser',
            email='other@example.com',
            password='testpass123'
        )
        client.force_login(other_user)

        response = client.get(reverse('appointments:detail', args=[appointment.pk]))
        assert response.status_code == 404  # Не должен видеть чужую запись

    def test_appointment_cancel_view(self, authenticated_client, appointment, user):
        """Тест отмены записи - ИСПРАВЛЕНО"""
        # Убедимся что пользователь является владельцем записи
        appointment.user = user
        appointment.status = 'pending'
        appointment.save()

        response = authenticated_client.post(
            reverse('appointments:cancel', args=[appointment.pk]),
            {'reason': 'Test reason'}
        )
        # После отмены должен быть редирект
        assert response.status_code == 302
        appointment.refresh_from_db()
        assert appointment.status == 'cancelled'