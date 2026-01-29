from django.urls import path
from . import views

app_name = "anamnesis"
urlpatterns = [
    path("", views.BuilderView.as_view(), name="builder"),
    path("add/", views.add_question, name="add_question"),
]
