import pytest
from apps.common.forms import ContactForm

class TestContactForm:
    def test_contact_form_valid_data(self):
        """Тест валидной формы обратной связи"""
        form_data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'subject': 'Test Subject',
            'message': 'Test message content'
        }
        form = ContactForm(data=form_data)
        assert form.is_valid()

    def test_contact_form_invalid_email(self):
        """Тест формы с невалидным email"""
        form_data = {
            'name': 'John Doe',
            'email': 'invalid-email',
            'subject': 'Test Subject',
            'message': 'Test message content'
        }
        form = ContactForm(data=form_data)
        assert not form.is_valid()
        assert 'email' in form.errors