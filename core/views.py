from datetime import datetime, time

from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.views.generic import TemplateView

from crm.models import Client, ClientFile, ClientNote
from workouts.models import ClientWorkout
from diets.models import ClientDiet
from logbook.models import ProgressRecord
from agenda.models import Appointment, Feedback


class LoginViewCustom(LoginView):
    template_name = "auth/login.html"


class LogoutViewCustom(LogoutView):
    pass


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "core/dashboard.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        events = []

        for w in ClientWorkout.objects.select_related("client", "plan").order_by("-applied_at")[:10]:
            events.append({"ts": w.applied_at, "label": "treino aplicado", "client": w.client, "detail": w.plan.name})

        for d in ClientDiet.objects.select_related("client", "plan").order_by("-applied_at")[:10]:
            events.append({"ts": d.applied_at, "label": "dieta aplicada", "client": d.client, "detail": d.plan.name})

        for p in ProgressRecord.objects.select_related("client").order_by("-date")[:10]:
            ts = timezone.make_aware(datetime.combine(p.date, time.min))
            detail = f"{p.weight_kg}kg" if p.weight_kg else "registro de progresso"
            events.append({"ts": ts, "label": "progresso", "client": p.client, "detail": detail})

        for f in ClientFile.objects.select_related("client").order_by("-uploaded_at")[:10]:
            label = "exame recebido" if f.kind == "exam" else "foto enviada"
            events.append({"ts": f.uploaded_at, "label": label, "client": f.client, "detail": f.title or "arquivo"})

        for n in ClientNote.objects.select_related("client").order_by("-created_at")[:10]:
            events.append({"ts": n.created_at, "label": "nota adicionada", "client": n.client, "detail": n.text[:60]})

        for fb in Feedback.objects.select_related("client").order_by("-created_at")[:10]:
            events.append({"ts": fb.created_at, "label": "mensagem registrada", "client": fb.client, "detail": fb.text[:60]})

        for a in Appointment.objects.select_related("client").order_by("-starts_at")[:10]:
            # Um evento pode existir sem cliente associado (client é NULL).
            # Evitamos quebrar o dashboard ao montar links.
            events.append({"ts": a.starts_at, "label": "evento", "client": a.client, "detail": a.title})

        events = sorted(events, key=lambda x: x["ts"], reverse=True)[:12]

        ctx["recent_events"] = events
        ctx["recent_clients"] = Client.objects.order_by("-created_at")[:6]
        return ctx
