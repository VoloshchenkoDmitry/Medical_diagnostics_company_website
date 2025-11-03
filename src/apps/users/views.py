"""
Users views module.
"""
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, TemplateView, UpdateView

from .forms import UserLoginForm, UserProfileForm, UserRegisterForm
from .models import User


class UserRegisterView(CreateView):
    """User registration view."""

    model = User
    form_class = UserRegisterForm
    template_name = "users/register.html"
    success_url = reverse_lazy("users:profile")  # Правильно - с namespace

    def form_valid(self, form):
        """Handle valid form submission."""
        response = super().form_valid(form)
        login(self.request, self.object)
        messages.success(self.request, _("Регистрация прошла успешно! Добро пожаловать!"))
        return response

    def form_invalid(self, form):
        """Handle invalid form submission."""
        messages.error(self.request, _("Пожалуйста, исправьте ошибки в форме."))
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        """Get context data for template."""
        context = super().get_context_data(**kwargs)
        context["page_title"] = _("Регистрация - Медицинский Диагностический Центр")
        return context


class UserLoginView(LoginView):
    """User login view."""

    form_class = UserLoginForm
    template_name = "users/login.html"
    redirect_authenticated_user = True

    def get_success_url(self):
        """Get success URL after login."""
        messages.success(self.request, _("Вы успешно вошли в систему!"))
        return reverse_lazy("users:profile")  # Правильно - с namespace

    def form_invalid(self, form):
        """Handle invalid form submission."""
        messages.error(self.request, _("Неверное имя пользователя или пароль."))
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        """Get context data for template."""
        context = super().get_context_data(**kwargs)
        context["page_title"] = _("Вход - Медицинский Диагностический Центр")
        return context


class UserLogoutView(LogoutView):
    """User logout view."""

    next_page = reverse_lazy("common:home")  # Правильно - с namespace

    def dispatch(self, request, *args, **kwargs):
        """Handle logout dispatch."""
        messages.success(request, _("Вы успешно вышли из системы."))
        return super().dispatch(request, *args, **kwargs)


class UserProfileView(LoginRequiredMixin, UpdateView):
    """User profile view."""

    model = User
    form_class = UserProfileForm
    template_name = "users/profile.html"
    success_url = reverse_lazy("users:profile")  # Правильно - с namespace

    def get_object(self):
        """Get user object."""
        return self.request.user

    def form_valid(self, form):
        """Handle valid form submission."""
        messages.success(self.request, _("Профиль успешно обновлен!"))
        return super().form_valid(form)

    def form_invalid(self, form):
        """Handle invalid form submission."""
        messages.error(self.request, _("Пожалуйста, исправьте ошибки в форме."))
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        """Get context data for template."""
        context = super().get_context_data(**kwargs)
        context["page_title"] = _("Личный кабинет - Медицинский Диагностический Центр")
        return context


class ProfileDashboardView(LoginRequiredMixin, TemplateView):
    """Profile dashboard view."""

    template_name = "users/dashboard.html"

    def get_context_data(self, **kwargs):
        """Get context data for template."""
        context = super().get_context_data(**kwargs)
        context["page_title"] = _("Личный кабинет - Медицинский Диагностический Центр")
        return context
