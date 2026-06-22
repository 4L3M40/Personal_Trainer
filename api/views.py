from django.db import models
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from workouts.models import WorkoutAssignment, WorkoutSession, ExerciseSetLog, WorkoutExercise
from workouts.serializers import WorkoutPlanDetailSerializer, WorkoutSessionSerializer
from django.shortcuts import get_object_or_404
from accounts.models import PersonalProfile
from logbook.models import ProgressRecord


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "is_staff": user.is_staff,
        })


class StudentMeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        sp = request.user.student_profile
        return Response({
            "user_id": request.user.id,
            "username": request.user.username,
            "client_id": sp.client_id,
            "personal_id": sp.personal_id,
        })


class StudentWorkoutTodayView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        sp = request.user.student_profile
        today = timezone.localdate()

        qs = (
            WorkoutAssignment.objects.filter(
                client_id=sp.client_id,
                is_active=True,
            )
            .filter(
                models.Q(start_date__isnull=True) | models.Q(start_date__lte=today)
            )
            .filter(
                models.Q(end_date__isnull=True) | models.Q(end_date__gte=today)
            )
            .select_related("workout")
            .order_by("-start_date", "-id")
        )

        assignment = qs.first()

        if not assignment:
            return Response(
                {"detail": "Nenhum treino ativo encontrado para este aluno."},
                status=404,
            )

        workout_data = WorkoutPlanDetailSerializer(assignment.workout).data

        return Response({
            "assignment": {
                "id": assignment.id,
                "start_date": str(assignment.start_date) if assignment.start_date else None,
                "end_date": str(assignment.end_date) if assignment.end_date else None,
            },
            "workout": workout_data,
        })


class StudentStartWorkoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, assignment_id: int):
        sp = request.user.student_profile

        assignment = get_object_or_404(
            WorkoutAssignment,
            id=assignment_id,
            client_id=sp.client_id,
            is_active=True,
        )

        today = timezone.localdate()

        session, created = WorkoutSession.objects.get_or_create(
            assignment=assignment,
            performed_on=today,
            defaults={
                "notes": request.data.get("notes", ""),
            },
        )

        if session.finished_at:
            session.finished_at = None
            session.save(update_fields=["finished_at"])

        return Response({
            "created": created,
            "session": WorkoutSessionSerializer(session).data,
        })


class StudentLogSetView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, session_id: int):
        sp = request.user.student_profile
        session = get_object_or_404(
            WorkoutSession,
            id=session_id,
            assignment__client_id=sp.client_id,
        )

        workout_exercise_id = request.data.get("workout_exercise")
        if not workout_exercise_id:
            return Response({"detail": "workout_exercise é obrigatório."}, status=400)

        workout_exercise = get_object_or_404(
            WorkoutExercise,
            id=workout_exercise_id,
            day__plan_id=session.assignment.workout_id,
        )

        log = ExerciseSetLog.objects.create(
            session=session,
            workout_exercise=workout_exercise,
            set_number=int(request.data.get("set_number", 1)),
            reps_done=request.data.get("reps_done"),
            load_used=str(request.data.get("load_used", "")),
            is_done=bool(request.data.get("is_done", True)),
            notes=str(request.data.get("notes", "")),
        )

        return Response({
            "log_id": log.id,
            "session": WorkoutSessionSerializer(session).data,
        }, status=201)


class StudentFinishWorkoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, session_id: int):
        sp = request.user.student_profile
        session = get_object_or_404(
            WorkoutSession,
            id=session_id,
            assignment__client_id=sp.client_id,
        )

        session.finished_at = timezone.now()
        if "notes" in request.data:
            session.notes = request.data.get("notes", "")
        session.save(update_fields=["finished_at", "notes"])

        return Response({
            "session": WorkoutSessionSerializer(session).data
        })


def _get_personal_profile(user):
    return get_object_or_404(PersonalProfile, user=user)


class PersonalStudentSessionsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, client_id: int):
        personal = _get_personal_profile(request.user)

        sessions = (
            WorkoutSession.objects.filter(
                assignment__personal=personal,
                assignment__client_id=client_id,
            )
            .select_related("assignment", "assignment__workout")
            .prefetch_related("set_logs", "set_logs__workout_exercise", "set_logs__workout_exercise__exercise")
            .order_by("-performed_on", "-id")
        )

        data = WorkoutSessionSerializer(sessions, many=True).data
        return Response({"client_id": client_id, "sessions": data})


class PersonalSessionDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, session_id: int):
        personal = _get_personal_profile(request.user)

        session = get_object_or_404(
            WorkoutSession.objects.select_related("assignment", "assignment__workout").prefetch_related(
                "set_logs",
                "set_logs__workout_exercise",
                "set_logs__workout_exercise__exercise",
                "set_logs__workout_exercise__day",
            ),
            id=session_id,
            assignment__personal=personal,
        )

        return Response({"session": WorkoutSessionSerializer(session).data})


class StudentSessionsListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        sp = request.user.student_profile
        sessions = (
            WorkoutSession.objects.filter(assignment__client_id=sp.client_id)
            .select_related("assignment", "assignment__workout")
            .prefetch_related(
                "set_logs",
                "set_logs__workout_exercise",
                "set_logs__workout_exercise__exercise",
                "set_logs__workout_exercise__day",
            )
            .order_by("-performed_on", "-id")[:30]
        )
        return Response({"sessions": WorkoutSessionSerializer(sessions, many=True).data})


class StudentHomeView(APIView):
    """Dashboard da Home do app do aluno: junta peso, treino, dieta e resumo do dia."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        sp = request.user.student_profile
        client_id = sp.client_id
        today = timezone.localdate()
        month_start = today.replace(day=1)

        last_weight = (
            ProgressRecord.objects.filter(client_id=client_id, weight_kg__isnull=False)
            .order_by("-date", "-id")
            .first()
        )
        weight_data = {
            "current_kg": float(last_weight.weight_kg) if last_weight else None,
            "recorded_on": str(last_weight.date) if last_weight else None,
        }

        assignment = (
            WorkoutAssignment.objects.filter(client_id=client_id, is_active=True)
            .filter(models.Q(start_date__isnull=True) | models.Q(start_date__lte=today))
            .filter(models.Q(end_date__isnull=True) | models.Q(end_date__gte=today))
            .select_related("workout")
            .order_by("-start_date", "-id")
            .first()
        )

        days = []
        today_workout = None
        if assignment:
            days = list(assignment.workout.days.order_by("order"))
            day_label = None
            if days:
                finished_count = assignment.sessions.filter(finished_at__isnull=False).count()
                day_label = days[finished_count % len(days)].label

            today_workout = {
                "assignment_id": assignment.id,
                "plan_name": assignment.workout.name,
                "day_label": day_label,
            }

        from diets.models import ClientDiet, MealLog
        
        client_diet = (
            ClientDiet.objects.filter(client_id=client_id, is_current=True)
            .select_related("plan")
            .order_by("-applied_at")
            .first()
        )

        today_diet = None
        meals_total_today = 0
        meals_done_today = 0
        if client_diet:
            meals_total_today = client_diet.plan.meals.count()
            meals_done_today = MealLog.objects.filter(client_id=client_id, date=today).count()
            today_diet = {
                "plan_name": client_diet.plan.name,
                "target_kcal": client_diet.plan.total_kcal,
            }

        workouts_done_month = WorkoutSession.objects.filter(
            assignment__client_id=client_id,
            finished_at__isnull=False,
            performed_on__gte=month_start,
            performed_on__lte=today,
        ).count()

        workouts_target_month = len(days) * 4 if days else 0

        from crm.models import ClientFile
        
        last_photo = (
            ClientFile.objects.filter(client_id=client_id, kind=ClientFile.Kind.PHOTO)
            .order_by("-uploaded_at")
            .first()
        )

        return Response({
            "student_name": request.user.first_name or request.user.username,
            "weight": weight_data,
            "today_workout": today_workout,
            "today_diet": today_diet,
            "summary": {
                "workouts_done_month": workouts_done_month,
                "workouts_target_month": workouts_target_month,
                "meals_done_today": meals_done_today,
                "meals_total_today": meals_total_today,
                "last_photo_upload": str(last_photo.uploaded_at.date()) if last_photo else None,
            },
        })


class StudentRegisterWeightView(APIView):
    """Cria/atualiza o peso do aluno para hoje (botão 'Registrar Peso' da Home)."""

    permission_classes = [IsAuthenticated]

    def post(self, request):
        sp = request.user.student_profile
        weight = request.data.get("weight_kg")
        if weight is None:
            return Response({"detail": "weight_kg é obrigatório."}, status=400)

        try:
            weight = float(weight)
        except (TypeError, ValueError):
            return Response({"detail": "weight_kg inválido."}, status=400)

        today = timezone.localdate()
        record, _ = ProgressRecord.objects.update_or_create(
            client_id=sp.client_id,
            date=today,
            defaults={"weight_kg": weight},
        )

        return Response({
            "current_kg": float(record.weight_kg),
            "recorded_on": str(record.date),
        })