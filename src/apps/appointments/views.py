"""
Appointments views module.
"""
import datetime

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DetailView, ListView, View

from apps.services.models import Service

from .forms import AppointmentCancelForm, AppointmentForm
from .models import Appointment


class AppointmentCreateView(LoginRequiredMixin, CreateView):
    """View for creating new appointments."""

    model = Appointment
    form_class = AppointmentForm
    template_name = "appointments/create.html"

    def get_initial(self):
        """Get initial data for form."""
        initial = super().get_initial()
        service_slug = self.kwargs.get("service_slug")
        if service_slug:
            service = get_object_or_404(Service, slug=service_slug, is_active=True)
            initial["service"] = service
        return initial

    def get_form_kwargs(self):
        """Get form kwargs."""
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        service_slug = self.kwargs.get("service_slug")
        if service_slug:
            service = get_object_or_404(Service, slug=service_slug, is_active=True)
            kwargs["service"] = service
        return kwargs

    def form_valid(self, form):
        """Handle valid form submission."""
        response = super().form_valid(form)
        messages.success(
            self.request,
            _("Запись успешно создана! Мы свяжемся с вами для подтверждения."),
        )
        return response

    def get_context_data(self, **kwargs):
        """Get context data for template."""
        context = super().get_context_data(**kwargs)
        service_slug = self.kwargs.get("service_slug")
        if service_slug:
            service = get_object_or_404(Service, slug=service_slug, is_active=True)
            context["service"] = service
            context["page_title"] = f"Запись на {service.name}"
        return context

    def get_success_url(self):
        """Get success URL."""
        return reverse_lazy("appointments:list")  # Правильно - с namespace


class AppointmentListView(LoginRequiredMixin, ListView):
    """View for listing user appointments."""

    model = Appointment
    template_name = "appointments/list.html"
    context_object_name = "appointments"
    paginate_by = 10

    def get_queryset(self):
        """Get queryset for appointments."""
        return Appointment.objects.filter(user=self.request.user).select_related("service")

    def get_context_data(self, **kwargs):
        """Get context data for template."""
        context = super().get_context_data(**kwargs)
        context["page_title"] = _("Мои записи на прием")

        # Statistics
        appointments = self.get_queryset()
        context["total_appointments"] = appointments.count()
        context["upcoming_appointments"] = appointments.filter(
            status__in=["pending", "confirmed"],
        ).count()
        context["completed_appointments"] = appointments.filter(
            status="completed",
        ).count()

        return context


class AppointmentDetailView(LoginRequiredMixin, DetailView):
    """View for appointment details."""

    model = Appointment
    template_name = "appointments/detail.html"
    context_object_name = "appointment"

    def get_queryset(self):
        """Get queryset for appointments."""
        return Appointment.objects.filter(user=self.request.user).select_related("service")

    def get_context_data(self, **kwargs):
        """Get context data for template."""
        context = super().get_context_data(**kwargs)
        context["page_title"] = _("Детали записи")
        context["cancel_form"] = AppointmentCancelForm()
        return context


class AppointmentCancelView(LoginRequiredMixin, View):
    """View for cancelling appointments."""

    def post(self, request, pk):
        """Handle POST request for cancellation."""
        from django.shortcuts import redirect

        appointment = get_object_or_404(Appointment, pk=pk, user=request.user)

        if not appointment.can_be_cancelled:
            messages.error(request, _("Невозможно отменить эту запись."))
            return redirect("appointments:detail", pk=pk)

        form = AppointmentCancelForm(request.POST)
        if form.is_valid():
            appointment.status = "cancelled"
            appointment.admin_notes = f"Отменено пользователем. Причина: {form.cleaned_data.get('reason', 'Не указана')}"
            appointment.save()

            messages.success(request, _("Запись успешно отменена."))
            return redirect("appointments:list")

        messages.error(request, _("Произошла ошибка при отмене записи."))
        return redirect("appointments:detail", pk=pk)


class AvailableTimeSlotsView(LoginRequiredMixin, View):
    """API view for getting available time slots."""

    def get(self, request, service_slug):
        """Handle GET request for available time slots."""
        date = request.GET.get("date")
        if not date:
            return JsonResponse({"error": "Date parameter is required"}, status=400)

        try:
            selected_date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
        except ValueError:
            return JsonResponse({"error": "Invalid date format"}, status=400)

        # Get booked time slots
        booked_slots = Appointment.objects.filter(
            desired_date=selected_date,
            status__in=["pending", "confirmed"],
        ).values_list("desired_time", flat=True)

        # All possible slots
        all_slots = [slot[0] for slot in Appointment.TIME_SLOTS]

        # Available slots
        available_slots = [slot for slot in all_slots if slot not in booked_slots]

        return JsonResponse({"date": date, "available_slots": available_slots})
