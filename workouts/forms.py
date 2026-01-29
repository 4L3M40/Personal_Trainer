from django import forms
from .models import WorkoutPlan, WorkoutDay, WorkoutExercise, ClientWorkout

class WorkoutPlanForm(forms.ModelForm):
    class Meta:
        model = WorkoutPlan
        fields = ["name","tags","is_active"]

class WorkoutDayForm(forms.ModelForm):
    class Meta:
        model = WorkoutDay
        fields = ["label","order"]

class WorkoutExerciseForm(forms.ModelForm):
    class Meta:
        model = WorkoutExercise
        fields = ["exercise","sets","reps","suggested_load","rest_seconds","notes"]

class ClientWorkoutForm(forms.ModelForm):
    class Meta:
        model = ClientWorkout
        fields = ["client","plan","is_current"]
