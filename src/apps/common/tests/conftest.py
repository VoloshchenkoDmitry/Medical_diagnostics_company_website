"""
Pytest configuration for common app tests.
"""
import pytest
from django.test import RequestFactory


@pytest.fixture
def contact_form_data():
    """Contact form test data."""
    return {
        "name": "Test User",
        "email": "test@example.com",
        "subject": "Test Subject",
        "message": "Test message content",
    }
