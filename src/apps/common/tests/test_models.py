"""
Tests for common models.
"""
import pytest

from apps.common.models import ContactSubmission


@pytest.mark.django_db
class TestContactSubmissionModel:
    """Test cases for ContactSubmission model."""

    def test_create_contact_submission(self):
        """Test creating a contact submission."""
        contact = ContactSubmission.objects.create(
            name="John Doe",
            email="john@example.com",
            subject="Test Subject",
            message="Test message content",
            status="new",
        )

        assert contact.name == "John Doe"
        assert contact.email == "john@example.com"
        assert contact.status == "new"
        assert contact.created_at is not None
        assert contact.updated_at is not None

    def test_contact_submission_str_representation(self):
        """Test string representation of contact submission."""
        contact = ContactSubmission.objects.create(
            name="John Doe",
            email="john@example.com",
            subject="Test Subject",
            message="Test message content",
        )
        expected_str = f"{contact.name} - {contact.subject}"
        assert str(contact) == expected_str

    def test_contact_submission_ordering(self):
        """Test that contacts are ordered by creation date descending."""
        contact1 = ContactSubmission.objects.create(
            name="John Doe",
            email="john@example.com",
            subject="Test Subject 1",
            message="Test message content",
        )

        contact2 = ContactSubmission.objects.create(
            name="Jane Doe",
            email="jane@example.com",
            subject="Test Subject 2",
            message="Test message content",
        )

        contacts = ContactSubmission.objects.all()
        assert contacts[0] == contact2  # Most recent first
        assert contacts[1] == contact1

    def test_contact_submission_default_status(self):
        """Test that status defaults to 'new'."""
        contact = ContactSubmission.objects.create(
            name="John Doe",
            email="john@example.com",
            subject="Test Subject",
            message="Test message content",
        )
        assert contact.status == "new"
