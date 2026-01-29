from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from .models import Appointment

class CalendarView(LoginRequiredMixin, TemplateView):
    template_name = "agenda/calendar.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        # Protótipo: lista simples (sem engine de calendário ainda)
        ctx["events"] = Appointment.objects.order_by("starts_at")[:10]
        return ctx
