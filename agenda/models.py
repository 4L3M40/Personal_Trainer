from django.db import models
from crm.models import Client

class Appointment(models.Model):
    """Evento de agenda (consulta, avaliação, revisão)."""
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=160)
    starts_at = models.DateTimeField()
    ends_at = models.DateTimeField()

    def __str__(self) -> str:
        return self.title

class Feedback(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="feedbacks")
    created_at = models.DateTimeField(auto_now_add=True)
    text = models.TextField()

class Alert(models.Model):
    """Alertas simples para o dashboard."""
    title = models.CharField(max_length=160)
    is_open = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
