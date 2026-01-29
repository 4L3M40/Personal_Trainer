from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from .models import DietPlan, Meal
from .forms import DietPlanForm, MealForm, MealItemForm

class DietPlanListView(LoginRequiredMixin, ListView):
    model = DietPlan
    template_name = "diets/diet_list.html"
    context_object_name = "plans"

    def get_queryset(self):
        return DietPlan.objects.order_by("-id")

class DietPlanCreateView(LoginRequiredMixin, CreateView):
    model = DietPlan
    form_class = DietPlanForm
    template_name = "diets/diet_form.html"
    success_url = reverse_lazy("diets:diet_list")

class DietPlanUpdateView(LoginRequiredMixin, UpdateView):
    model = DietPlan
    form_class = DietPlanForm
    template_name = "diets/diet_form.html"

    def get_success_url(self):
        return reverse("diets:diet_detail", kwargs={"pk": self.object.pk})

class DietPlanDetailView(LoginRequiredMixin, DetailView):
    model = DietPlan
    template_name = "diets/diet_detail.html"
    context_object_name = "plan"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        meals = self.object.meals.prefetch_related("items__food").all()
        ctx["meals"] = meals
        meal_id = self.request.GET.get("meal")
        ctx["selected_meal"] = None
        if meal_id:
            ctx["selected_meal"] = get_object_or_404(Meal, pk=meal_id, plan=self.object)
        elif meals:
            ctx["selected_meal"] = meals[0]

        ctx["meal_form"] = MealForm()
        ctx["item_form"] = MealItemForm()
        return ctx

def add_meal(request, pk):
    plan = get_object_or_404(DietPlan, pk=pk)
    form = MealForm(request.POST)
    if form.is_valid():
        meal = form.save(commit=False)
        meal.plan = plan
        meal.save()
        messages.success(request, "Refeição adicionada.")
    return redirect("diets:diet_detail", pk=pk)

def add_food(request, pk):
    plan = get_object_or_404(DietPlan, pk=pk)
    meal_id = request.POST.get("meal_id")
    meal = get_object_or_404(Meal, pk=meal_id, plan=plan)
    form = MealItemForm(request.POST)
    if form.is_valid():
        item = form.save(commit=False)
        item.meal = meal
        item.save()
        messages.success(request, "Alimento adicionado na refeição.")
    return redirect(f"{reverse('diets:diet_detail', kwargs={'pk': pk})}?meal={meal.pk}")
