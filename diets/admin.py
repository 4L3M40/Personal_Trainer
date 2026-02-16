from django.contrib import admin
from .models import DietPlan, Meal, MealItem, ClientDiet

class MealItemInline(admin.TabularInline):
    model = MealItem
    extra = 0

class MealInline(admin.TabularInline):
    model = Meal
    extra = 0

@admin.register(DietPlan)
class DietPlanAdmin(admin.ModelAdmin):
    list_display = ("name","total_kcal","is_active")
    search_fields = ("name",)
    inlines = [MealInline]

@admin.register(Meal)
class MealAdmin(admin.ModelAdmin):
    list_display = ("plan","name","order")
    inlines = [MealItemInline]

@admin.register(ClientDiet)
class ClientDietAdmin(admin.ModelAdmin):
    list_display = ("client","plan","is_current","applied_at")
    list_filter = ("is_current",)
