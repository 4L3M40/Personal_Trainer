from django.db import models
from crm.models import Client
from library.models import Exercise

class WorkoutPlan(models.Model):
    """Treino modelo (ex.: ABC Cutting)."""
    name = models.CharField(max_length=120)
    tags = models.CharField(max_length=200, blank=True, help_text="Ex.: Hipertrofia, ABC")
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.name

class WorkoutDay(models.Model):
    """Dia dentro de um treino (Dia A, B, C...)."""
    plan = models.ForeignKey(WorkoutPlan, on_delete=models.CASCADE, related_name="days")
    label = models.CharField(max_length=40)  # "Dia A"
    order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ["order"]

    def __str__(self) -> str:
        return f"{self.plan.name} • {self.label}"

class WorkoutExercise(models.Model):
    """Exercício configurado dentro de um dia."""
    day = models.ForeignKey(WorkoutDay, on_delete=models.CASCADE, related_name="items")
    exercise = models.ForeignKey(Exercise, on_delete=models.PROTECT)
    sets = models.PositiveIntegerField(default=4)
    reps = models.CharField(max_length=20, default="10-12")
    suggested_load = models.CharField(max_length=40, blank=True)
    rest_seconds = models.PositiveIntegerField(default=60)
    notes = models.CharField(max_length=240, blank=True)

    def __str__(self) -> str:
        return f"{self.exercise.name} ({self.sets}x{self.reps})"

class ClientWorkout(models.Model):
    """Treino aplicado para um cliente (vincula plano)."""
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="workouts")
    plan = models.ForeignKey(WorkoutPlan, on_delete=models.PROTECT)
    applied_at = models.DateTimeField(auto_now_add=True)
    is_current = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f"{self.client.full_name} • {self.plan.name}"
