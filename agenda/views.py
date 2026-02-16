from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import TemplateView, CreateView, UpdateView

from .models import Appointment
from .forms import AppointmentForm


class CalendarView(LoginRequiredMixin, TemplateView):
    template_name = "agenda/calendar.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        now = timezone.now()
        ctx["events"] = Appointment.objects.order_by("starts_at")[:50]
        ctx["upcoming"] = Appointment.objects.filter(starts_at__gte=now).order_by("starts_at")[:20]
        return ctx


class AppointmentCreateView(LoginRequiredMixin, CreateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = "agenda/appointment_form.html"
    success_url = reverse_lazy("agenda:calendar")

    def get_initial(self):
        initial = super().get_initial()
        client_id = self.request.GET.get("client")
        if client_id:
            initial["client"] = client_id
        return initial

    def form_valid(self, form):
        messages.success(self.request, "Evento criado.")
        return super().form_valid(form)


class AppointmentUpdateView(LoginRequiredMixin, UpdateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = "agenda/appointment_form.html"
    success_url = reverse_lazy("agenda:calendar")

    def form_valid(self, form):
        messages.success(self.request, "Evento atualizado.")
        return super().form_valid(form)


def delete_appointment(request, pk):
    appt = get_object_or_404(Appointment, pk=pk)
    if request.method == "POST":
        appt.delete()
        messages.success(request, "Evento removido.")
    return redirect("agenda:calendar")
