from django.urls import path
from . import views

app_name = "workouts"

urlpatterns = [
    path("", views.WorkoutPlanListView.as_view(), name="workout_list"),
    path("novo/", views.WorkoutPlanCreateView.as_view(), name="workout_create"),
    path("<int:pk>/", views.WorkoutPlanDetailView.as_view(), name="workout_detail"),
    path("<int:pk>/editar/", views.WorkoutPlanUpdateView.as_view(), name="workout_update"),

    path("<int:pk>/add-dia/", views.add_day, name="add_day"),
    path("<int:pk>/dia/<int:day_id>/delete/", views.delete_day, name="day_delete"),

    path("<int:pk>/add-exercicio/", views.add_exercise, name="add_exercise"),
    path("<int:pk>/exercicio/<int:item_id>/update/", views.update_exercise, name="exercise_update"),
    path("<int:pk>/exercicio/<int:item_id>/delete/", views.delete_exercise, name="exercise_delete"),

    path("<int:pk>/aplicar/", views.apply_to_client, name="apply_to_client"),
]
