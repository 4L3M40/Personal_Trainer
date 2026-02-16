from django.urls import path
from . import views

app_name = "agenda"

urlpatterns = [
    path("", views.CalendarView.as_view(), name="calendar"),
    path("novo/", views.AppointmentCreateView.as_view(), name="appointment_create"),
    path("<int:pk>/editar/", views.AppointmentUpdateView.as_view(), name="appointment_update"),
    path("<int:pk>/delete/", views.delete_appointment, name="appointment_delete"),
]
