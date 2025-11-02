from django.shortcuts import render
from django.views.generic import TemplateView, FormView
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import ContactForm


class HomeView(TemplateView):
    template_name = 'common/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Главная - Медицинский Диагностический Центр'
        return context


class AboutView(TemplateView):
    template_name = 'common/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'О компании - Медицинский Диагностический Центр'
        return context


class ContactsView(FormView):
    template_name = 'common/contacts.html'
    form_class = ContactForm
    success_url = reverse_lazy('common:contacts')  # Убедитесь что здесь common:contacts

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Контакты - Медицинский Диагностический Центр'
        return context

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Ваше сообщение успешно отправлено! Мы свяжемся с вами в ближайшее время.')
        return super().form_valid(form)


# Обработчики ошибок
def handler400(request, exception):
    return render(request, 'common/400.html', status=400)


def handler403(request, exception):
    return render(request, 'common/403.html', status=403)


def handler404(request, exception):
    return render(request, 'common/404.html', status=404)


def handler500(request):
    return render(request, 'common/500.html', status=500)
