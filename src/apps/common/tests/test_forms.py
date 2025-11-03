"""
Tests for common forms.
"""
import pytest
from django.test import RequestFactory

from apps.common.forms import ContactForm
from apps.common.models import ContactSubmission


@pytest.mark.django_db
class TestContactForm:
    """Test cases for ContactForm."""

    def test_contact_form_valid_data(self, contact_form_data):
        """Test contact form with valid data."""
        form = ContactForm(data=contact_form_data)
        assert form.is_valid() is True

    def test_contact_form_missing_name(self, contact_form_data):
        """Test contact form with missing name."""
        invalid_data = contact_form_data.copy()
        invalid_data.pop("name")
        form = ContactForm(data=invalid_data)
        assert form.is_valid() is False
        assert "name" in form.errors

    def test_contact_form_invalid_email(self, contact_form_data):
        """Test contact form with invalid email."""
        invalid_data = contact_form_data.copy()
        invalid_data["email"] = "invalid-email"
        form = ContactForm(data=invalid_data)
        assert form.is_valid() is False
        assert "email" in form.errors

    def test_contact_form_save_with_request(self, contact_form_data, rf):
        """Test saving contact form with request information."""
        request = rf.post("/contacts/")
        request.META["HTTP_USER_AGENT"] = "Test Browser"
        request.META["REMOTE_ADDR"] = "127.0.0.1"

        form = ContactForm(data=contact_form_data)
        assert form.is_valid() is True

        contact = form.save(request=request)

        assert contact.name == "Test User"
        assert contact.ip_address == "127.0.0.1"
        assert contact.user_agent == "Test Browser"

    def test_contact_form_save_without_request(self, contact_form_data):
        """Test saving contact form without request information."""
        form = ContactForm(data=contact_form_data)
        assert form.is_valid() is True

        contact = form.save()

        assert contact.name == "Test User"
        assert contact.ip_address is None
        assert contact.user_agent == ""
