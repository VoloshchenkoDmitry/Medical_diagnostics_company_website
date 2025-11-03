"""
Common views module.
"""
from django.contrib import messages
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView

from .forms import ContactForm


class HomeView(TemplateView):
    """Home page view."""

    template_name = "common/index.html"

    def get_context_data(self, **kwargs):
        """Get context data for template."""
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Главная - Медицинский Диагностический Центр"
        return context


class AboutView(TemplateView):
    """About page view."""

    template_name = "common/about.html"

    def get_context_data(self, **kwargs):
        """Get context data for template."""
        context = super().get_context_data(**kwargs)
        context["page_title"] = "О компании - Медицинский Диагностический Центр"
        return context


class ContactsView(FormView):
    """Contacts page view."""

    template_name = "common/contacts.html"
    form_class = ContactForm
    success_url = reverse_lazy("common:contacts")  # ИСПРАВЛЕНО: добавлен namespace

    def get_context_data(self, **kwargs):
        """Get context data for template."""
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Контакты - Медицинский Диагностический Центр"
        return context

    def form_valid(self, form):
        """Handle valid form submission."""
        # Сохраняем форму с информацией о запросе
        form.save(request=self.request)
        messages.success(
            self.request,
            "Ваше сообщение успешно отправлено! Мы свяжемся с вами в ближайшее время.",
        )
        return super().form_valid(form)
