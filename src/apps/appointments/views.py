from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import CreateView, ListView, DetailView, View
from django.utils.translation import gettext_lazy as _
from django.db.models import Q
from .models import Appointment
from .forms import AppointmentForm, AppointmentCancelForm
from apps.services.models import Service


class AppointmentCreateView(LoginRequiredMixin, CreateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = 'appointments/create.html'

    def get_initial(self):
        initial = super().get_initial()
        service_slug = self.kwargs.get('service_slug')
        if service_slug:
            service = get_object_or_404(Service, slug=service_slug, is_active=True)
            initial['service'] = service
        return initial

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        service_slug = self.kwargs.get('service_slug')
        if service_slug:
            service = get_object_or_404(Service, slug=service_slug, is_active=True)
            kwargs['service'] = service
        return kwargs

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request,
            _('Запись успешно создана! Мы свяжемся с вами для подтверждения.')
        )
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        service_slug = self.kwargs.get('service_slug')
        if service_slug:
            service = get_object_or_404(Service, slug=service_slug, is_active=True)
            context['service'] = service
            context['page_title'] = f'Запись на {service.name}'
        return context

    def get_success_url(self):
        return reverse_lazy('appointments:list')


class AppointmentListView(LoginRequiredMixin, ListView):
    model = Appointment
    template_name = 'appointments/list.html'
    context_object_name = 'appointments'
    paginate_by = 10

    def get_queryset(self):
        return Appointment.objects.filter(user=self.request.user).select_related('service')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = _('Мои записи на прием')

        # Статистика
        appointments = self.get_queryset()
        context['total_appointments'] = appointments.count()
        context['upcoming_appointments'] = appointments.filter(
            status__in=['pending', 'confirmed']
        ).count()
        context['completed_appointments'] = appointments.filter(
            status='completed'
        ).count()

        return context


class AppointmentDetailView(LoginRequiredMixin, DetailView):
    model = Appointment
    template_name = 'appointments/detail.html'
    context_object_name = 'appointment'

    def get_queryset(self):
        return Appointment.objects.filter(user=self.request.user).select_related('service')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = _('Детали записи')
        context['cancel_form'] = AppointmentCancelForm()
        return context


class AppointmentCancelView(LoginRequiredMixin, View):
    def post(self, request, pk):
        appointment = get_object_or_404(
            Appointment,
            pk=pk,
            user=request.user
        )

        if not appointment.can_be_cancelled:
            messages.error(
                request,
                _('Невозможно отменить эту запись.')
            )
            return redirect('appointments:detail', pk=pk)

        form = AppointmentCancelForm(request.POST)
        if form.is_valid():
            appointment.status = 'cancelled'
            appointment.admin_notes = f"Отменено пользователем. Причина: {form.cleaned_data.get('reason', 'Не указана')}"
            appointment.save()

            messages.success(
                request,
                _('Запись успешно отменена.')
            )
            return redirect('appointments:list')

        messages.error(
            request,
            _('Произошла ошибка при отмене записи.')
        )
        return redirect('appointments:detail', pk=pk)


class AvailableTimeSlotsView(LoginRequiredMixin, View):
    def get(self, request, service_slug):
        date = request.GET.get('date')
        if not date:
            return JsonResponse({'error': 'Date parameter is required'}, status=400)

        try:
            selected_date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
        except ValueError:
            return JsonResponse({'error': 'Invalid date format'}, status=400)

        # Получаем занятые временные слоты
        booked_slots = Appointment.objects.filter(
            desired_date=selected_date,
            status__in=['pending', 'confirmed']
        ).values_list('desired_time', flat=True)

        # Все возможные слоты
        all_slots = [slot[0] for slot in Appointment.TIME_SLOTS]

        # Доступные слоты
        available_slots = [slot for slot in all_slots if slot not in booked_slots]

        return JsonResponse({
            'date': date,
            'available_slots': available_slots
        })