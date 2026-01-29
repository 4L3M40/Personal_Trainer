from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import TemplateView
from .models import AnamnesisQuestion
from .forms import QuestionForm

class BuilderView(LoginRequiredMixin, TemplateView):
    template_name = "anamnesis/builder.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["questions"] = AnamnesisQuestion.objects.order_by("-created_at")
        ctx["form"] = QuestionForm()
        return ctx

def add_question(request):
    form = QuestionForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, "Pergunta adicionada.")
    return redirect("anamnesis:builder")
