"""
Tests for users models.
"""
import pytest
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()


@pytest.mark.django_db
class TestUserModel:
    """Test cases for User model."""

    def test_create_user(self, user_data):
        """Test creating a regular user."""
        user = User.objects.create_user(**user_data)

        assert user.username == "testuser"
        assert user.email == "test@example.com"
        assert user.first_name == "John"
        assert user.last_name == "Doe"
        assert user.is_active is True
        assert user.is_staff is False
        assert user.is_superuser is False

    def test_create_superuser(self):
        """Test creating a superuser."""
        superuser = User.objects.create_superuser(username="admin", email="admin@example.com", password="adminpass123")

        assert superuser.username == "admin"
        assert superuser.email == "admin@example.com"
        assert superuser.is_active is True
        assert superuser.is_staff is True
        assert superuser.is_superuser is True

    def test_user_str_representation(self, test_user):
        """Test string representation of user."""
        assert str(test_user) == "testuser"

    def test_user_get_full_name(self, test_user):
        """Test get_full_name method."""
        assert test_user.get_full_name() == "John Doe"

    def test_user_get_full_name_no_names(self):
        """Test get_full_name when first and last names are empty."""
        user = User.objects.create_user(
            username="user1",
            email="user1@example.com",
            password="testpass123",
            first_name="",
            last_name="",
        )
        assert user.get_full_name() == "user1"

    def test_user_email_unique(self):
        """Test that email must be unique."""
        User.objects.create_user(username="user1", email="test@example.com", password="testpass123")

        with pytest.raises(Exception):  # Should raise IntegrityError
            User.objects.create_user(
                username="user2",
                email="test@example.com",  # Same email
                password="testpass123",
            )

    def test_user_ordering(self):
        """Test that users are ordered by creation date."""
        user1 = User.objects.create_user(username="user1", email="user1@example.com", password="testpass123")

        user2 = User.objects.create_user(username="user2", email="user2@example.com", password="testpass123")

        users = User.objects.all()
        assert users[0] == user2  # Most recent first
        assert users[1] == user1
