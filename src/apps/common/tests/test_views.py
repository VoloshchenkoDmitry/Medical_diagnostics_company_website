"""
Tests for common views.
"""
import pytest
from django.urls import reverse


@pytest.mark.django_db
class TestCommonViews:
    """Test cases for common views."""

    def test_home_view_status_code(self, client):
        """Test that home page returns 200."""
        response = client.get(reverse("common:home"))
        assert response.status_code == 200

    def test_about_view_status_code(self, client):
        """Test that about page returns 200."""
        response = client.get(reverse("common:about"))
        assert response.status_code == 200

    def test_contacts_view_status_code(self, client):
        """Test that contacts page returns 200."""
        response = client.get(reverse("common:contacts"))
        assert response.status_code == 200

    def test_contact_form_submission(self, client):
        """Test successful contact form submission."""
        form_data = {
            "name": "Test User",
            "email": "test@example.com",
            "subject": "Test Subject",
            "message": "Test message content",
        }

        response = client.post(reverse("common:contacts"), data=form_data)

        # Should redirect to same page with success message
        assert response.status_code == 302
        assert response.url == reverse("common:contacts")

        # Check that contact submission was created
        from apps.common.models import ContactSubmission

        assert ContactSubmission.objects.count() == 1
        contact = ContactSubmission.objects.first()
        assert contact.name == "Test User"
        assert contact.email == "test@example.com"

    def test_contact_form_invalid_data(self, client):
        """Test contact form with invalid data."""
        invalid_data = {
            "name": "Test User",
            "email": "invalid-email",  # Invalid email
            "subject": "Test Subject",
            "message": "Test message content",
        }

        response = client.post(reverse("common:contacts"), data=invalid_data)

        # Should stay on same page with form errors
        assert response.status_code == 200
        assert "form" in response.context
        assert not response.context["form"].is_valid()

    def test_home_view_context(self, client):
        """Test that home view has correct context."""
        response = client.get(reverse("common:home"))
        assert "page_title" in response.context
