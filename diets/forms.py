from django import forms
from .models import DietPlan, Meal, MealItem

class DietPlanForm(forms.ModelForm):
    class Meta:
        model = DietPlan
        fields = ["name","total_kcal","is_active"]

class MealForm(forms.ModelForm):
    class Meta:
        model = Meal
        fields = ["name","order"]

class MealItemForm(forms.ModelForm):
    class Meta:
        model = MealItem
        fields = ["food","quantity_label","kcal","protein_g","carbs_g","fats_g","notes"]
