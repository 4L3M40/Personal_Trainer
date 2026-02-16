from django import forms
from .models import DietPlan, Meal, MealItem, ClientDiet

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


class ApplyDietForm(forms.ModelForm):
    """Form enxuto para aplicar uma dieta modelo em um cliente."""

    class Meta:
        model = ClientDiet
        fields = ["plan"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["plan"].queryset = DietPlan.objects.filter(is_active=True).order_by("name")


class ApplyDietToClientForm(forms.Form):
    client = forms.ModelChoiceField(queryset=None)

    def __init__(self, *args, **kwargs):
        from crm.models import Client
        super().__init__(*args, **kwargs)
        self.fields["client"].queryset = Client.objects.order_by("full_name")
