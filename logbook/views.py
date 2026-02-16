from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

class LogbookHomeView(LoginRequiredMixin, TemplateView):
    template_name = "logbook/home.html"
