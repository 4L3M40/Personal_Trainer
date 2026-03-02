from django.db import models
from django.utils import timezone
from accounts.models import PersonalProfile
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


class WorkoutAssignment(models.Model):
    personal = models.ForeignKey(
        PersonalProfile,
        on_delete=models.CASCADE,
        related_name="workout_assignments",
    )
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name="workout_assignments",
    )
    workout = models.ForeignKey(
        WorkoutPlan,
        on_delete=models.PROTECT,
        related_name="assignments",
    )

    start_date = models.DateField(default=timezone.localdate)
    end_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-start_date", "-id"]

    def __str__(self):
        return f"{self.client.full_name} • {self.workout.name}"


class WorkoutSession(models.Model):
    assignment = models.ForeignKey(
        WorkoutAssignment,
        on_delete=models.CASCADE,
        related_name="sessions",
    )
    performed_on = models.DateField(default=timezone.localdate)
    started_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    notes = models.CharField(max_length=240, blank=True)

    class Meta:
        ordering = ["-performed_on", "-id"]
        unique_together = ("assignment", "performed_on")

    def __str__(self):
        return f"Session {self.assignment_id} on {self.performed_on}"


class ExerciseSetLog(models.Model):
    session = models.ForeignKey(
        WorkoutSession,
        on_delete=models.CASCADE,
        related_name="set_logs",
    )
    workout_exercise = models.ForeignKey(
        WorkoutExercise,
        on_delete=models.PROTECT,
        related_name="set_logs",
    )

    set_number = models.PositiveIntegerField(default=1)
    reps_done = models.PositiveIntegerField(null=True, blank=True)
    load_used = models.CharField(max_length=40, blank=True)
    is_done = models.BooleanField(default=True)
    notes = models.CharField(max_length=240, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["set_number", "id"]

    def __str__(self):
        return f"SetLog session={self.session_id} ex={self.workout_exercise_id} set={self.set_number}"