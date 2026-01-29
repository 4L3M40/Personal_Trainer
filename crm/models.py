from django.db import models

class Plan(models.Model):
    """Plano/objetivo principal (ex.: Cutting, Bulking, Manutenção)."""
    name = models.CharField(max_length=80, unique=True)

    def __str__(self) -> str:
        return self.name

class Client(models.Model):
    """Cliente do personal (dados essenciais para o protótipo)."""

    class Status(models.TextChoices):
        ACTIVE = "active", "Ativo"
        PAUSED = "paused", "Pausado"
        ARCHIVED = "archived", "Arquivado"

    full_name = models.CharField("Nome", max_length=160)
    age = models.PositiveIntegerField("Idade", default=0)
    weight_kg = models.DecimalField("Peso (kg)", max_digits=5, decimal_places=1, default=0)
    height_m = models.DecimalField("Altura (m)", max_digits=4, decimal_places=2, default=0)
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.ACTIVE)
    plan = models.ForeignKey(Plan, on_delete=models.SET_NULL, null=True, blank=True)
    last_activity_at = models.DateField("Última atividade", null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.full_name
