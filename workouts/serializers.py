from rest_framework import serializers

from .models import (
    WorkoutPlan,
    WorkoutDay,
    WorkoutExercise,
    WorkoutSession,
    ExerciseSetLog,
)


# ----------- Plano de Treino (para o app do aluno) -----------

class WorkoutExerciseSerializer(serializers.ModelSerializer):
    exercise_name = serializers.CharField(source="exercise.name", read_only=True)

    class Meta:
        model = WorkoutExercise
        fields = [
            "id",
            "exercise",
            "exercise_name",
            "sets",
            "reps",
            "suggested_load",
            "rest_seconds",
            "notes",
        ]


class WorkoutDaySerializer(serializers.ModelSerializer):
    items = WorkoutExerciseSerializer(many=True, read_only=True)

    class Meta:
        model = WorkoutDay
        fields = ["id", "label", "order", "items"]


class WorkoutPlanDetailSerializer(serializers.ModelSerializer):
    days = WorkoutDaySerializer(many=True, read_only=True)

    class Meta:
        model = WorkoutPlan
        fields = ["id", "name", "tags", "is_active", "days"]


# ----------- Execução do treino (sessões e logs) -----------

class ExerciseSetLogSerializer(serializers.ModelSerializer):
    day_label = serializers.CharField(source="workout_exercise.day.label", read_only=True)
    exercise_name = serializers.CharField(source="workout_exercise.exercise.name", read_only=True)

    class Meta:
        model = ExerciseSetLog
        fields = [
            "id",
            "workout_exercise",
            "day_label",
            "exercise_name",
            "set_number",
            "reps_done",
            "load_used",
            "is_done",
            "notes",
            "created_at",
        ]


class WorkoutSessionSerializer(serializers.ModelSerializer):
    set_logs = ExerciseSetLogSerializer(many=True, read_only=True)
    workout_name = serializers.CharField(source="assignment.workout.name", read_only=True)
    client_id = serializers.IntegerField(source="assignment.client_id", read_only=True)

    class Meta:
        model = WorkoutSession
        fields = [
            "id",
            "assignment",
            "client_id",
            "workout_name",
            "performed_on",
            "started_at",
            "finished_at",
            "notes",
            "set_logs",
        ]