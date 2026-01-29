from django.urls import path
from .views import LogbookHomeView

app_name = "logbook"
urlpatterns = [
    path("", LogbookHomeView.as_view(), name="home"),
]
