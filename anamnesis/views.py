from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import TemplateView

from .models import AnamnesisQuestion
from .forms import QuestionForm


class BuilderView(LoginRequiredMixin, TemplateView):
    template_name = "anamnesis/builder.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["questions"] = AnamnesisQuestion.objects.order_by("-created_at")
        ctx["form"] = QuestionForm()

        edit_id = self.request.GET.get("edit")
        ctx["edit_question"] = None
        ctx["edit_form"] = None
        if edit_id:
            q = get_object_or_404(AnamnesisQuestion, pk=edit_id)
            ctx["edit_question"] = q
            ctx["edit_form"] = QuestionForm(instance=q)
        return ctx


def add_question(request):
    form = QuestionForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, "Pergunta adicionada.")
    return redirect("anamnesis:builder")


def update_question(request, pk):
    q = get_object_or_404(AnamnesisQuestion, pk=pk)
    form = QuestionForm(request.POST, instance=q)
    if form.is_valid():
        form.save()
        messages.success(request, "Pergunta atualizada.")
    return redirect("anamnesis:builder")


def delete_question(request, pk):
    q = get_object_or_404(AnamnesisQuestion, pk=pk)
    if request.method == "POST":
        q.delete()
        messages.success(request, "Pergunta removida.")
    return redirect("anamnesis:builder")
