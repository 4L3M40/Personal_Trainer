from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from .models import Client
from .forms import ClientForm

class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    template_name = "crm/client_list.html"
    context_object_name = "clients"
    paginate_by = 20

    def get_queryset(self):
        qs = super().get_queryset().select_related("plan").order_by("-created_at")
        q = self.request.GET.get("q")
        if q:
            qs = qs.filter(full_name__icontains=q)
        return qs

class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client
    template_name = "crm/client_detail.html"
    context_object_name = "client"

class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    template_name = "crm/client_form.html"
    success_url = reverse_lazy("crm:client_list")

class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    template_name = "crm/client_form.html"

    def get_success_url(self):
        return reverse_lazy("crm:client_detail", kwargs={"pk": self.object.pk})
