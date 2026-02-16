from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from core.views import LoginViewCustom, LogoutViewCustom

urlpatterns = [
    path("admin/", admin.site.urls),

    # Auth simples (protótipo)
    path("login/", LoginViewCustom.as_view(), name="login"),
    path("logout/", LogoutViewCustom.as_view(), name="logout"),

    # Módulos
    path("", include("core.urls")),
    path("crm/", include("crm.urls")),
    path("biblioteca/", include("library.urls")),
    path("treinos/", include("workouts.urls")),
    path("dietas/", include("diets.urls")),
    path("anamnese/", include("anamnesis.urls")),
    path("logbook/", include("logbook.urls")),
    path("agenda/", include("agenda.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
