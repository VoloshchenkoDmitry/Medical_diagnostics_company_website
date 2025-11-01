from django import forms
from django.conf import settings
from django.core.mail import send_mail

from .models import ContactSubmission


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactSubmission
        fields = ["name", "email", "subject", "message"]
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Введите ваше имя"}
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "Введите ваш email"}
            ),
            "subject": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Тема сообщения"}
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
        instance = super().save(commit=False)

        # Сохраняем информацию о запросе
        if request:
            instance.ip_address = self.get_client_ip(request)
            instance.user_agent = request.META.get("HTTP_USER_AGENT", "")

        if commit:
            instance.save()

            # Отправляем email уведомление (в продакшене)
            if not settings.DEBUG:
                try:
                    send_mail(
                        subject=f"Новое сообщение с формы обратной связи: {instance.subject}",
                        message=f"""
Имя: {instance.name}
Email: {instance.email}
Тема: {instance.subject}
Сообщение: {instance.message}

IP: {instance.ip_address}
Время: {instance.created_at}
                        """,
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[settings.CONTACT_EMAIL],
                        fail_silently=True,
                    )
                except Exception as e:
                    # Логируем ошибку, но не прерываем выполнение
                    print(f"Ошибка отправки email: {e}")

        return instance

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip
