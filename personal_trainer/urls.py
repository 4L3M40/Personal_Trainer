from django.contrib import admin
from django.urls import path, include

from core.views import LoginViewCustom, LogoutViewCustom

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("admin/", admin.site.urls),

    # Auth simples (protótipo - site do personal)
    path("login/", LoginViewCustom.as_view(), name="login"),
    path("logout/", LogoutViewCustom.as_view(), name="logout"),

    # API (mobile do aluno)
    path("api/v1/auth/login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/v1/auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/v1/", include("api.urls")),

    # Site do personal (templates)
    path("", include("core.urls")),
    path("crm/", include("crm.urls")),
    path("biblioteca/", include("library.urls")),
    path("treinos/", include("workouts.urls")),
    path("dietas/", include("diets.urls")),
    path("anamnese/", include("anamnesis.urls")),
    path("logbook/", include("logbook.urls")),
    path("agenda/", include("agenda.urls")),
]