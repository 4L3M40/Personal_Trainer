from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

class LoginViewCustom(LoginView):
    template_name = "auth/login.html"

class LogoutViewCustom(LogoutView):
    pass

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "core/dashboard.html"
