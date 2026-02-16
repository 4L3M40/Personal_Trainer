from django.db import models
from crm.models import Client
from library.models import Food

class DietPlan(models.Model):
    """Dieta modelo (ex.: Cutting 1800kcal)."""
    name = models.CharField(max_length=120)
    total_kcal = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.name

class Meal(models.Model):
    plan = models.ForeignKey(DietPlan, on_delete=models.CASCADE, related_name="meals")
    name = models.CharField(max_length=80)  # Café da manhã, Almoço, etc.
    order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ["order"]

    def __str__(self) -> str:
        return f"{self.plan.name} • {self.name}"

class MealItem(models.Model):
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE, related_name="items")
    food = models.ForeignKey(Food, on_delete=models.PROTECT)
    quantity_label = models.CharField(max_length=40, default="100g")
    kcal = models.PositiveIntegerField(default=0)
    protein_g = models.DecimalField(max_digits=5, decimal_places=1, default=0)
    carbs_g = models.DecimalField(max_digits=5, decimal_places=1, default=0)
    fats_g = models.DecimalField(max_digits=5, decimal_places=1, default=0)
    notes = models.CharField(max_length=240, blank=True)

    def __str__(self) -> str:
        return f"{self.food.name} • {self.quantity_label}"

class ClientDiet(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="diets")
    plan = models.ForeignKey(DietPlan, on_delete=models.PROTECT)
    applied_at = models.DateTimeField(auto_now_add=True)
    is_current = models.BooleanField(default=True)
