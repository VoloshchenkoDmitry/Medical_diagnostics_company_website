"""
Common forms module.
"""
from django import forms
from django.core.mail import send_mail

from .models import ContactSubmission


class ContactForm(forms.ModelForm):
    """Contact form for user inquiries."""

    class Meta:
        """Meta options for ContactForm."""

        model = ContactSubmission
        fields = ["name", "email", "subject", "message"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Введите ваше имя",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Введите ваш email",
                }
            ),
            "subject": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Тема сообщения",
                }
            ),
            "message": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 5,
                    "placeholder": "Введите ваше сообщение...",
                }
            ),
        }

    def save(self, request=None, commit=True):
        """Save contact submission with request info."""
        instance = super().save(commit=False)

        # Save request information
        if request:
            instance.ip_address = self.get_client_ip(request)
            instance.user_agent = request.META.get("HTTP_USER_AGENT", "")

        if commit:
            instance.save()

        return instance

    def get_client_ip(self, request):
        """Get client IP address from request."""
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip
