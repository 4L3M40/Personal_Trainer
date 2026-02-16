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


class ApplyWorkoutForm(forms.ModelForm):
    """Form enxuto para aplicar um treino modelo em um cliente."""

    class Meta:
        model = ClientWorkout
        fields = ["plan"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["plan"].queryset = WorkoutPlan.objects.filter(is_active=True).order_by("name")


class ApplyWorkoutToClientForm(forms.Form):
    """Aplicar o treino atual (plan) para um cliente."""

    client = forms.ModelChoiceField(queryset=None)

    def __init__(self, *args, **kwargs):
        from crm.models import Client
        super().__init__(*args, **kwargs)
        self.fields["client"].queryset = Client.objects.order_by("full_name")
