from django.contrib import admin
from .models import WorkoutPlan, WorkoutDay, WorkoutExercise, ClientWorkout

class WorkoutExerciseInline(admin.TabularInline):
    model = WorkoutExercise
    extra = 0

class WorkoutDayInline(admin.TabularInline):
    model = WorkoutDay
    extra = 0

@admin.register(WorkoutPlan)
class WorkoutPlanAdmin(admin.ModelAdmin):
    list_display = ("name","is_active")
    search_fields = ("name",)
    inlines = [WorkoutDayInline]

@admin.register(WorkoutDay)
class WorkoutDayAdmin(admin.ModelAdmin):
    list_display = ("plan","label","order")
    inlines = [WorkoutExerciseInline]

@admin.register(ClientWorkout)
class ClientWorkoutAdmin(admin.ModelAdmin):
    list_display = ("client","plan","is_current","applied_at")
    list_filter = ("is_current",)
