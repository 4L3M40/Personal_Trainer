from django.urls import path
from .views import CalendarView

app_name = "agenda"
urlpatterns = [
    path("", CalendarView.as_view(), name="calendar"),
]
