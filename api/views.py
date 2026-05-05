from django.db import models
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from workouts.models import WorkoutAssignment
from workouts.serializers import WorkoutPlanDetailSerializer
from django.shortcuts import get_object_or_404
from django.utils import timezone
from workouts.models import WorkoutSession, ExerciseSetLog, WorkoutExercise, WorkoutAssignment
from workouts.serializers import WorkoutSessionSerializer
from accounts.models import PersonalProfile


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
        sp = request.user.student_profile  # só existe para aluno
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

        # Se já existia uma sessão finalizada no mesmo dia,
        # reabre para permitir testar novamente no app.
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

        # garante que o workout_exercise pertence ao plano do assignment
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