from django.urls import path
from . import views

app_name = "library"

urlpatterns = [
    path("", views.ExerciseListView.as_view(), name="exercises"),
    path("exercicios/", views.ExerciseListView.as_view(), name="exercises"),
    path("exercicios/novo/", views.ExerciseCreateView.as_view(), name="exercise_create"),
    path("exercicios/<int:pk>/editar/", views.ExerciseUpdateView.as_view(), name="exercise_update"),

    path("alimentos/", views.FoodListView.as_view(), name="foods"),
    path("alimentos/novo/", views.FoodCreateView.as_view(), name="food_create"),
    path("alimentos/<int:pk>/editar/", views.FoodUpdateView.as_view(), name="food_update"),
]
