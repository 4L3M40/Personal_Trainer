from django import forms
from .models import Exercise, Food

class ExerciseForm(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = ["name","muscle_group","notes"]

class FoodForm(forms.ModelForm):
    class Meta:
        model = Food
        fields = ["name","portion_label","kcal","protein_g","carbs_g","fats_g"]
