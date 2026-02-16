from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView

from .models import Exercise, Food
from .forms import ExerciseForm, FoodForm


class ExerciseListView(LoginRequiredMixin, ListView):
    model = Exercise
    template_name = "library/exercises.html"
    context_object_name = "items"

    def get_queryset(self):
        qs = super().get_queryset().order_by("name")
        q = self.request.GET.get("q")
        if q:
            qs = qs.filter(name__icontains=q)
        return qs


class ExerciseCreateView(LoginRequiredMixin, CreateView):
    model = Exercise
    form_class = ExerciseForm
    template_name = "library/exercise_form.html"
    success_url = reverse_lazy("library:exercises")


class ExerciseUpdateView(LoginRequiredMixin, UpdateView):
    model = Exercise
    form_class = ExerciseForm
    template_name = "library/exercise_form.html"
    success_url = reverse_lazy("library:exercises")


def delete_exercise(request, pk):
    ex = get_object_or_404(Exercise, pk=pk)
    if request.method == "POST":
        ex.delete()
        messages.success(request, "Exercício removido.")
    return redirect("library:exercises")


class FoodListView(LoginRequiredMixin, ListView):
    model = Food
    template_name = "library/foods.html"
    context_object_name = "items"

    def get_queryset(self):
        qs = super().get_queryset().order_by("name")
        q = self.request.GET.get("q")
        if q:
            qs = qs.filter(name__icontains=q)
        return qs


class FoodCreateView(LoginRequiredMixin, CreateView):
    model = Food
    form_class = FoodForm
    template_name = "library/food_form.html"
    success_url = reverse_lazy("library:foods")


class FoodUpdateView(LoginRequiredMixin, UpdateView):
    model = Food
    form_class = FoodForm
    template_name = "library/food_form.html"
    success_url = reverse_lazy("library:foods")


def delete_food(request, pk):
    f = get_object_or_404(Food, pk=pk)
    if request.method == "POST":
        f.delete()
        messages.success(request, "Alimento removido.")
    return redirect("library:foods")
