from django.contrib import messages
from datetime import datetime, time
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, DetailView, CreateView, UpdateView, TemplateView

from .models import Client, ClientFile, ClientNote, ClientAnamnesisAnswer
from .forms import ClientForm, ClientFileForm, ClientNoteForm

from workouts.models import WorkoutPlan, ClientWorkout
from workouts.forms import ApplyWorkoutForm
from diets.models import DietPlan, ClientDiet
from diets.forms import ApplyDietForm
from logbook.models import ProgressRecord
from logbook.forms import ProgressRecordForm
from anamnesis.models import AnamnesisQuestion
from agenda.models import Appointment, Feedback


class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    template_name = "crm/client_list.html"
    context_object_name = "clients"
    paginate_by = 20

    def get_queryset(self):
        qs = super().get_queryset().select_related("plan").order_by("-created_at")
        q = self.request.GET.get("q")
        if q:
            qs = qs.filter(full_name__icontains=q)
        return qs


class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client
    template_name = "crm/client_detail.html"
    context_object_name = "client"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        client = self.object
        ctx["active_tab"] = "overview"
        ctx["current_workout"] = client.workouts.select_related("plan").filter(is_current=True).order_by("-applied_at").first()
        ctx["current_diet"] = client.diets.select_related("plan").filter(is_current=True).order_by("-applied_at").first()
        ctx["latest_progress"] = client.progress.all()[:8]
        ctx["latest_files"] = client.files.all()[:6]
        ctx["latest_notes"] = client.notes.all()[:4]
        ctx["next_appointments"] = Appointment.objects.filter(client=client, starts_at__gte=timezone.now()).order_by("starts_at")[:5]
        return ctx


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    template_name = "crm/client_form.html"
    success_url = reverse_lazy("crm:client_list")


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    template_name = "crm/client_form.html"

    def get_success_url(self):
        return reverse_lazy("crm:client_detail", kwargs={"pk": self.object.pk})


class ClientWorkoutsView(LoginRequiredMixin, TemplateView):
    template_name = "crm/client_workouts.html"

    def get_client(self):
        return get_object_or_404(Client, pk=self.kwargs["pk"])

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        client = self.get_client()
        ctx["client"] = client
        ctx["current_workout"] = client.workouts.select_related("plan").filter(is_current=True).first()
        ctx["history"] = client.workouts.select_related("plan").order_by("-applied_at")[:20]
        ctx["plans"] = WorkoutPlan.objects.filter(is_active=True).order_by("name")
        ctx["form"] = ApplyWorkoutForm()
        ctx["active_tab"] = "treinos"
        return ctx

    def post(self, request, *args, **kwargs):
        client = self.get_client()
        form = ApplyWorkoutForm(request.POST)
        if form.is_valid():
            ClientWorkout.objects.filter(client=client, is_current=True).update(is_current=False)
            cw = form.save(commit=False)
            cw.client = client
            cw.is_current = True
            cw.save()
            client.last_activity_at = timezone.localdate()
            client.save(update_fields=["last_activity_at"])
            messages.success(request, "Treino aplicado ao cliente.")
        return redirect("crm:client_workouts", pk=client.pk)


class ClientDietsView(LoginRequiredMixin, TemplateView):
    template_name = "crm/client_diets.html"

    def get_client(self):
        return get_object_or_404(Client, pk=self.kwargs["pk"])

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        client = self.get_client()
        ctx["client"] = client
        ctx["current_diet"] = client.diets.select_related("plan").filter(is_current=True).first()
        ctx["history"] = client.diets.select_related("plan").order_by("-applied_at")[:20]
        ctx["plans"] = DietPlan.objects.filter(is_active=True).order_by("name")
        ctx["form"] = ApplyDietForm()
        ctx["active_tab"] = "dietas"
        return ctx

    def post(self, request, *args, **kwargs):
        client = self.get_client()
        form = ApplyDietForm(request.POST)
        if form.is_valid():
            ClientDiet.objects.filter(client=client, is_current=True).update(is_current=False)
            cd = form.save(commit=False)
            cd.client = client
            cd.is_current = True
            cd.save()
            client.last_activity_at = timezone.localdate()
            client.save(update_fields=["last_activity_at"])
            messages.success(request, "Dieta aplicada ao cliente.")
        return redirect("crm:client_diets", pk=client.pk)


class ClientProgressView(LoginRequiredMixin, TemplateView):
    template_name = "crm/client_progress.html"

    def get_client(self):
        return get_object_or_404(Client, pk=self.kwargs["pk"])

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        client = self.get_client()
        ctx["client"] = client
        ctx["records"] = client.progress.all()[:50]
        ctx["form"] = ProgressRecordForm()
        ctx["active_tab"] = "progresso"
        return ctx

    def post(self, request, *args, **kwargs):
        client = self.get_client()
        form = ProgressRecordForm(request.POST)
        if form.is_valid():
            rec = form.save(commit=False)
            rec.client = client
            rec.save()
            client.last_activity_at = timezone.localdate()
            client.save(update_fields=["last_activity_at"])
            messages.success(request, "Registro adicionado.")
        return redirect("crm:client_progress", pk=client.pk)


class ClientAnamnesisView(LoginRequiredMixin, TemplateView):
    template_name = "crm/client_anamnesis.html"

    def get_client(self):
        return get_object_or_404(Client, pk=self.kwargs["pk"])

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        client = self.get_client()
        questions = AnamnesisQuestion.objects.order_by("created_at")
        answers = {
            a.question_id: a.value
            for a in ClientAnamnesisAnswer.objects.filter(client=client, question__in=questions)
        }
        ctx.update(
            {
                "client": client,
                "questions": questions,
                "answers": answers,
                "active_tab": "anamnese",
            }
        )
        return ctx

    def post(self, request, *args, **kwargs):
        client = self.get_client()
        questions = AnamnesisQuestion.objects.all()
        for q in questions:
            key = f"q_{q.pk}"
            value = (request.POST.get(key) or "").strip()
            obj, _ = ClientAnamnesisAnswer.objects.get_or_create(client=client, question=q)
            obj.value = value
            obj.save()
        client.last_activity_at = timezone.localdate()
        client.save(update_fields=["last_activity_at"])
        messages.success(request, "Anamnese salva.")
        return redirect("crm:client_anamnesis", pk=client.pk)


class ClientFilesView(LoginRequiredMixin, TemplateView):
    template_name = "crm/client_files.html"
    kind = None

    @classmethod
    def as_view(cls, **initkwargs):
        return super().as_view(**initkwargs)

    def get_client(self):
        return get_object_or_404(Client, pk=self.kwargs["pk"])

    def get_kind(self):
        if not self.kind:
            raise Http404
        if self.kind not in ("exam", "photo"):
            raise Http404
        return self.kind

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        client = self.get_client()
        kind = self.get_kind()
        ctx["client"] = client
        ctx["kind"] = kind
        ctx["items"] = client.files.filter(kind=kind)
        ctx["form"] = ClientFileForm()
        ctx["active_tab"] = "exames" if kind == "exam" else "fotos"
        return ctx

    def post(self, request, *args, **kwargs):
        client = self.get_client()
        kind = self.get_kind()
        form = ClientFileForm(request.POST, request.FILES)
        if form.is_valid():
            cf = form.save(commit=False)
            cf.client = client
            cf.kind = kind
            cf.save()
            client.last_activity_at = timezone.localdate()
            client.save(update_fields=["last_activity_at"])
            messages.success(request, "Arquivo enviado.")
        return redirect("crm:client_exams" if kind == "exam" else "crm:client_photos", pk=client.pk)


def delete_client_file(request, pk, file_id):
    client = get_object_or_404(Client, pk=pk)
    f = get_object_or_404(ClientFile, pk=file_id, client=client)
    if request.method == "POST":
        f.file.delete(save=False)
        f.delete()
        messages.success(request, "Arquivo removido.")
    return redirect("crm:client_exams" if f.kind == "exam" else "crm:client_photos", pk=client.pk)


class ClientNotesView(LoginRequiredMixin, TemplateView):
    template_name = "crm/client_notes.html"

    def get_client(self):
        return get_object_or_404(Client, pk=self.kwargs["pk"])

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        client = self.get_client()
        ctx["client"] = client
        ctx["items"] = client.notes.all()[:100]
        ctx["form"] = ClientNoteForm()
        ctx["active_tab"] = "notas"
        return ctx

    def post(self, request, *args, **kwargs):
        client = self.get_client()
        form = ClientNoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.client = client
            note.save()
            client.last_activity_at = timezone.localdate()
            client.save(update_fields=["last_activity_at"])
            messages.success(request, "Nota adicionada.")
        return redirect("crm:client_notes", pk=client.pk)


def delete_client_note(request, pk, note_id):
    client = get_object_or_404(Client, pk=pk)
    note = get_object_or_404(ClientNote, pk=note_id, client=client)
    if request.method == "POST":
        note.delete()
        messages.success(request, "Nota removida.")
    return redirect("crm:client_notes", pk=client.pk)


class ClientLogbookView(LoginRequiredMixin, TemplateView):
    template_name = "crm/client_logbook.html"

    def get_client(self):
        return get_object_or_404(Client, pk=self.kwargs["pk"])

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        client = self.get_client()

        # Timeline simples (últimos 40 itens)
        workouts = client.workouts.select_related("plan").order_by("-applied_at")[:10]
        diets = client.diets.select_related("plan").order_by("-applied_at")[:10]
        progress = client.progress.order_by("-date")[:10]
        files = client.files.order_by("-uploaded_at")[:10]
        notes = client.notes.order_by("-created_at")[:10]
        feedbacks = client.feedbacks.order_by("-created_at")[:10]
        appts = Appointment.objects.filter(client=client).order_by("-starts_at")[:10]

        events = []
        for w in workouts:
            events.append({"ts": w.applied_at, "type": "workout", "obj": w})
        for d in diets:
            events.append({"ts": d.applied_at, "type": "diet", "obj": d})
        for p in progress:
            # date -> datetime for ordering
            events.append({"ts": timezone.make_aware(datetime.combine(p.date, time.min)), "type": "progress", "obj": p})
        for f in files:
            events.append({"ts": f.uploaded_at, "type": f.kind, "obj": f})
        for n in notes:
            events.append({"ts": n.created_at, "type": "note", "obj": n})
        for fb in feedbacks:
            events.append({"ts": fb.created_at, "type": "feedback", "obj": fb})
        for a in appts:
            events.append({"ts": a.starts_at, "type": "appointment", "obj": a})

        events = sorted(events, key=lambda x: x["ts"], reverse=True)[:40]

        ctx.update(
            {
                "client": client,
                "events": events,
                "active_tab": "logbook",
            }
        )
        return ctx

    def post(self, request, *args, **kwargs):
        """Adicionar feedback rápido (mensagem/observação do personal para o cliente)."""
        client = self.get_client()
        text = (request.POST.get("text") or "").strip()
        if text:
            Feedback.objects.create(client=client, text=text)
            client.last_activity_at = timezone.localdate()
            client.save(update_fields=["last_activity_at"])
            messages.success(request, "Entrada adicionada no logbook.")
        return redirect("crm:client_logbook", pk=client.pk)
