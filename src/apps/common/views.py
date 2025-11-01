from django.contrib import messages

from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView
from .forms import ContactForm


class HomeView(TemplateView):
    template_name = "common/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Здесь позже добавим популярные услуги, акции и т.д.
        context["page_title"] = "Главная - Медицинский Диагностический Центр"
        return context


class AboutView(TemplateView):
    template_name = "common/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "О компании - Медицинский Диагностический Центр"
        return context


class ContactsView(FormView):
    template_name = "common/contacts.html"
    form_class = ContactForm
    success_url = reverse_lazy("contacts")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Контакты - Медицинский Диагностический Центр"
        return context

    def form_valid(self, form):
        # Передаем request в форму для сохранения дополнительной информации
        form.save(request=self.request)
        messages.success(
            self.request,
            "Ваше сообщение успешно отправлено! Мы свяжемся с вами в ближайшее время.",
        )
        return super().form_valid(form)
