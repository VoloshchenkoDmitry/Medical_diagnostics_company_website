from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.utils.translation import gettext_lazy as _

from .models import User


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(
        label=_("Email"),
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": _("Введите ваш email")}),
    )
    first_name = forms.CharField(
        max_length=30,
        required=True,
        label=_("Имя"),
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": _("Введите ваше имя")}),
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        label=_("Фамилия"),
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": _("Введите вашу фамилию")}),
    )
    phone = forms.CharField(
        max_length=20,
        required=False,
        label=_("Телефон"),
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": _("+7 (XXX) XXX-XX-XX")}),
    )

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "phone",
            "password1",
            "password2",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Настройка полей родительского класса
        self.fields["username"].widget.attrs.update({"class": "form-control", "placeholder": _("Введите имя пользователя")})
        self.fields["password1"].widget.attrs.update({"class": "form-control", "placeholder": _("Введите пароль")})
        self.fields["password2"].widget.attrs.update({"class": "form-control", "placeholder": _("Повторите пароль")})


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        label=_("Имя пользователя или Email"),
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": _("Введите имя пользователя или email"),
            }
        ),
    )
    password = forms.CharField(
        label=_("Пароль"),
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": _("Введите пароль")}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "phone",
            "date_of_birth",
            "gender",
            "address",
            "avatar",
        ]
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "phone": forms.TextInput(attrs={"class": "form-control"}),
            "date_of_birth": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "gender": forms.Select(attrs={"class": "form-control"}),
            "address": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError(_("Пользователь с таким email уже существует."))
        return email
