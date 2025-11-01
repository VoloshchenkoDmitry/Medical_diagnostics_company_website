import pytest


from apps.common.forms import ContactForm


class TestContactForm:
    """Тесты для формы обратной связи"""

    def test_contact_form_valid_data(self):
        """Тест формы с валидными данными"""
        form_data = {
            "name": "Тестовый Пользователь",
            "email": "test@example.com",
            "subject": "Тестовый вопрос",
            "message": "Это тестовое сообщение",
        }
        form = ContactForm(data=form_data)
        assert form.is_valid()

    def test_contact_form_invalid_email(self):
        """Тест формы с невалидным email"""
        form_data = {
            "name": "Тестовый Пользователь",
            "email": "invalid-email",
            "subject": "Тестовый вопрос",
            "message": "Это тестовое сообщение",
        }
        form = ContactForm(data=form_data)
        assert not form.is_valid()
        assert "email" in form.errors

    def test_contact_form_missing_required_fields(self):
        """Тест формы с отсутствующими обязательными полями"""
        form_data = {
            "name": "",  # Обязательное поле
            "email": "test@example.com",
            "subject": "Тестовый вопрос",
            "message": "Это тестовое сообщение",
        }
        form = ContactForm(data=form_data)
        assert not form.is_valid()
        assert "name" in form.errors
