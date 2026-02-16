from django.contrib import admin
from .models import Exercise, Food

@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ("name","muscle_group")
    search_fields = ("name","muscle_group")

@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    list_display = ("name","portion_label","kcal","protein_g","carbs_g","fats_g")
    search_fields = ("name",)
