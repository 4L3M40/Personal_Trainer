from django.urls import path
from . import views

app_name = "anamnesis"

urlpatterns = [
    path("", views.BuilderView.as_view(), name="builder"),
    path("add/", views.add_question, name="add_question"),
    path("<int:pk>/update/", views.update_question, name="update_question"),
    path("<int:pk>/delete/", views.delete_question, name="delete_question"),
]
