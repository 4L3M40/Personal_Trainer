from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from .models import WorkoutPlan, WorkoutDay, WorkoutExercise
from .forms import WorkoutPlanForm, WorkoutDayForm, WorkoutExerciseForm

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

        ctx["day_form"] = WorkoutDayForm()
        ctx["item_form"] = WorkoutExerciseForm()
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
