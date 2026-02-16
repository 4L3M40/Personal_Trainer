from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from .models import WorkoutPlan, WorkoutDay, WorkoutExercise, ClientWorkout
from .forms import WorkoutPlanForm, WorkoutDayForm, WorkoutExerciseForm, ApplyWorkoutToClientForm
from crm.models import Client


class WorkoutPlanListView(LoginRequiredMixin, ListView):
    model = WorkoutPlan
    template_name = "workouts/workout_list.html"
    context_object_name = "plans"

    def get_queryset(self):
        return WorkoutPlan.objects.order_by("-id")


class WorkoutPlanCreateView(LoginRequiredMixin, CreateView):
    model = WorkoutPlan
    form_class = WorkoutPlanForm
    template_name = "workouts/workout_form.html"
    success_url = reverse_lazy("workouts:workout_list")


class WorkoutPlanUpdateView(LoginRequiredMixin, UpdateView):
    model = WorkoutPlan
    form_class = WorkoutPlanForm
    template_name = "workouts/workout_form.html"

    def get_success_url(self):
        return reverse("workouts:workout_detail", kwargs={"pk": self.object.pk})


class WorkoutPlanDetailView(LoginRequiredMixin, DetailView):
    model = WorkoutPlan
    template_name = "workouts/workout_detail.html"
    context_object_name = "plan"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        days = self.object.days.prefetch_related("items__exercise").all()
        ctx["days"] = days
        ctx["selected_day"] = None
        day_id = self.request.GET.get("day")
        if day_id:
            ctx["selected_day"] = get_object_or_404(WorkoutDay, pk=day_id, plan=self.object)
        elif days:
            ctx["selected_day"] = days[0]

        ctx["selected_item"] = None
        item_id = self.request.GET.get("item")
        if item_id and ctx["selected_day"]:
            ctx["selected_item"] = get_object_or_404(WorkoutExercise, pk=item_id, day=ctx["selected_day"])

        ctx["day_form"] = WorkoutDayForm()
        ctx["item_form"] = WorkoutExerciseForm(instance=ctx["selected_item"]) if ctx["selected_item"] else WorkoutExerciseForm()
        ctx["apply_form"] = ApplyWorkoutToClientForm()
        ctx["clients"] = Client.objects.order_by("full_name")
        return ctx


def add_day(request, pk):
    plan = get_object_or_404(WorkoutPlan, pk=pk)
    form = WorkoutDayForm(request.POST)
    if form.is_valid():
        day = form.save(commit=False)
        day.plan = plan
        day.save()
        messages.success(request, "Dia adicionado ao treino.")
    return redirect("workouts:workout_detail", pk=pk)


def delete_day(request, pk, day_id):
    plan = get_object_or_404(WorkoutPlan, pk=pk)
    day = get_object_or_404(WorkoutDay, pk=day_id, plan=plan)
    if request.method == "POST":
        day.delete()
        messages.success(request, "Dia removido.")
    return redirect("workouts:workout_detail", pk=pk)


def add_exercise(request, pk):
    plan = get_object_or_404(WorkoutPlan, pk=pk)
    day_id = request.POST.get("day_id")
    day = get_object_or_404(WorkoutDay, pk=day_id, plan=plan)
    form = WorkoutExerciseForm(request.POST)
    if form.is_valid():
        item = form.save(commit=False)
        item.day = day
        item.save()
        messages.success(request, "Exercício adicionado ao dia.")
    return redirect(f"{reverse('workouts:workout_detail', kwargs={'pk': pk})}?day={day.pk}")


def update_exercise(request, pk, item_id):
    plan = get_object_or_404(WorkoutPlan, pk=pk)
    item = get_object_or_404(WorkoutExercise, pk=item_id, day__plan=plan)
    form = WorkoutExerciseForm(request.POST, instance=item)
    if form.is_valid():
        form.save()
        messages.success(request, "Exercício atualizado.")
    return redirect(f"{reverse('workouts:workout_detail', kwargs={'pk': pk})}?day={item.day.pk}&item={item.pk}")


def delete_exercise(request, pk, item_id):
    plan = get_object_or_404(WorkoutPlan, pk=pk)
    item = get_object_or_404(WorkoutExercise, pk=item_id, day__plan=plan)
    day_id = item.day_id
    if request.method == "POST":
        item.delete()
        messages.success(request, "Exercício removido.")
    return redirect(f"{reverse('workouts:workout_detail', kwargs={'pk': pk})}?day={day_id}")


def apply_to_client(request, pk):
    plan = get_object_or_404(WorkoutPlan, pk=pk)
    form = ApplyWorkoutToClientForm(request.POST)
    if form.is_valid():
        client = form.cleaned_data["client"]
        ClientWorkout.objects.filter(client=client, is_current=True).update(is_current=False)
        ClientWorkout.objects.create(client=client, plan=plan, is_current=True)
        messages.success(request, f"Treino '{plan.name}' aplicado para {client.full_name}.")
        return redirect("crm:client_workouts", pk=client.pk)
    messages.error(request, "Selecione um cliente.")
    return redirect("workouts:workout_detail", pk=pk)
