"""
Tests for users views.
"""
import pytest
from django.urls import reverse


@pytest.mark.django_db
class TestUserViews:
    """Test cases for user views."""

    def test_register_view_get(self, client):
        """Test GET request to register view."""
        response = client.get(reverse("users:register"))
        assert response.status_code == 200

    def test_register_view_post_success(self, client):
        """Test successful user registration."""
        register_data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password1": "complexpass123",
            "password2": "complexpass123",
            "first_name": "Jane",
            "last_name": "Smith",
        }

        response = client.post(reverse("users:register"), data=register_data)

        # Should redirect to profile page
        assert response.status_code == 302
        assert response.url == reverse("users:profile")

        # Check that user was created
        from django.contrib.auth import get_user_model

        User = get_user_model()
        assert User.objects.filter(username="newuser").exists()

    def test_login_view_get(self, client):
        """Test GET request to login view."""
        response = client.get(reverse("users:login"))
        assert response.status_code == 200

    def test_login_view_post_success(self, client, test_user):
        """Test successful user login."""
        login_data = {"username": "testuser", "password": "testpass123"}

        response = client.post(reverse("users:login"), data=login_data)

        # Should redirect to profile page
        assert response.status_code == 302
        assert response.url == reverse("users:profile")

    def test_profile_view_requires_login(self, client):
        """Test that profile view requires authentication."""
        response = client.get(reverse("users:profile"))

        # Should redirect to login page
        assert response.status_code == 302
        assert reverse("users:login") in response.url

    def test_profile_view_authenticated(self, authenticated_client):
        """Test profile view for authenticated user."""
        response = authenticated_client.get(reverse("users:profile"))
        assert response.status_code == 200

    def test_logout_view(self, authenticated_client):
        """Test user logout."""
        # Check that user is logged in
        response = authenticated_client.get(reverse("users:profile"))
        assert response.status_code == 200

        # Logout - use POST request
        response = authenticated_client.post(reverse("users:logout"))

        # Should redirect to home page
        assert response.status_code == 302
        assert response.url == reverse("common:home")
