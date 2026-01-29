from django.urls import path
from . import views

app_name = "diets"

urlpatterns = [
    path("", views.DietPlanListView.as_view(), name="diet_list"),
    path("novo/", views.DietPlanCreateView.as_view(), name="diet_create"),
    path("<int:pk>/", views.DietPlanDetailView.as_view(), name="diet_detail"),
    path("<int:pk>/editar/", views.DietPlanUpdateView.as_view(), name="diet_update"),

    path("<int:pk>/add-refeicao/", views.add_meal, name="add_meal"),
    path("<int:pk>/add-alimento/", views.add_food, name="add_food"),
]
