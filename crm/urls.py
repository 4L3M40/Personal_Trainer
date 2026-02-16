from django.urls import path
from . import views

app_name = "crm"

urlpatterns = [
    path("", views.ClientListView.as_view(), name="client_list"),
    path("novo/", views.ClientCreateView.as_view(), name="client_create"),
    path("<int:pk>/", views.ClientDetailView.as_view(), name="client_detail"),
    path("<int:pk>/treinos/", views.ClientWorkoutsView.as_view(), name="client_workouts"),
    path("<int:pk>/dietas/", views.ClientDietsView.as_view(), name="client_diets"),
    path("<int:pk>/progresso/", views.ClientProgressView.as_view(), name="client_progress"),

    path("<int:pk>/anamnese/", views.ClientAnamnesisView.as_view(), name="client_anamnesis"),
    path("<int:pk>/exames/", views.ClientFilesView.as_view(kind="exam"), name="client_exams"),
    path("<int:pk>/fotos/", views.ClientFilesView.as_view(kind="photo"), name="client_photos"),
    path("<int:pk>/notas/", views.ClientNotesView.as_view(), name="client_notes"),
    path("<int:pk>/logbook/", views.ClientLogbookView.as_view(), name="client_logbook"),

    path("<int:pk>/arquivos/<int:file_id>/delete/", views.delete_client_file, name="client_file_delete"),
    path("<int:pk>/notas/<int:note_id>/delete/", views.delete_client_note, name="client_note_delete"),

    path("<int:pk>/editar/", views.ClientUpdateView.as_view(), name="client_update"),
]
