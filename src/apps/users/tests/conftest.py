"""
Pytest configuration for users app tests.
"""
import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture
def user_data():
    """User test data."""
    return {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpass123",
        "first_name": "John",
        "last_name": "Doe",
    }


@pytest.fixture
def test_user(db, user_data):
    """Create a test user."""
    return User.objects.create_user(**user_data)


@pytest.fixture
def authenticated_client(client, test_user):
    """Create an authenticated test client."""
    client.force_login(test_user)
    return client


@pytest.fixture
def superuser_data():
    """Superuser test data."""
    return {
        "username": "admin",
        "email": "admin@example.com",
        "password": "adminpass123",
    }


@pytest.fixture
def test_superuser(db, superuser_data):
    """Create a test superuser."""
    return User.objects.create_superuser(**superuser_data)
