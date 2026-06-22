from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import MeView, StudentMeView, StudentWorkoutTodayView
from .views import StudentStartWorkoutView, StudentLogSetView, StudentFinishWorkoutView
from .views import PersonalStudentSessionsView, PersonalSessionDetailView
from .views import StudentSessionsListView
from .views import StudentHomeView, StudentRegisterWeightView


urlpatterns = [
    # 🔐 Autenticação
    path("auth/login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    
    # Rotas existentes
    path("me/", MeView.as_view(), name="me"),
    path("student/me/", StudentMeView.as_view(), name="student-me"),
    path("student/home/", StudentHomeView.as_view(), name="student-home"),
    path("student/weight/", StudentRegisterWeightView.as_view(), name="student-register-weight"),
    path("student/workouts/today/", StudentWorkoutTodayView.as_view(), name="student-workout-today"),

    path("student/workouts/<int:assignment_id>/start/", StudentStartWorkoutView.as_view(), name="student-start-workout"),
    path("student/sessions/<int:session_id>/log-set/", StudentLogSetView.as_view(), name="student-log-set"),
    path("student/sessions/<int:session_id>/finish/", StudentFinishWorkoutView.as_view(), name="student-finish-workout"),

    # Personal
    path("personal/students/<int:client_id>/sessions/", PersonalStudentSessionsView.as_view(), name="personal-student-sessions"),
    path("personal/sessions/<int:session_id>/", PersonalSessionDetailView.as_view(), name="personal-session-detail"),
    path("student/sessions/", StudentSessionsListView.as_view(), name="student-sessions"),
]