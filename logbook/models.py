from django.db import models
from crm.models import Client

class ProgressRecord(models.Model):
    """Registro simples de progresso (peso, medidas, observação)."""
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="progress")
    date = models.DateField()
    weight_kg = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    notes = models.CharField(max_length=240, blank=True)

    class Meta:
        ordering = ["-date"]

    def __str__(self) -> str:
        return f"{self.client.full_name} • {self.date}"
