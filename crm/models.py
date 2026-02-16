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


class ClientFile(models.Model):
    """Arquivos enviados para o cliente (exames, fotos, etc.)."""

    class Kind(models.TextChoices):
        EXAM = "exam", "Exame"
        PHOTO = "photo", "Foto"

    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="files")
    kind = models.CharField(max_length=10, choices=Kind.choices)
    title = models.CharField(max_length=160, blank=True)
    file = models.FileField(upload_to="client_files/%Y/%m/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-uploaded_at"]

    def __str__(self) -> str:
        return f"{self.client.full_name} • {self.get_kind_display()}"


class ClientNote(models.Model):
    """Notas internas do personal sobre o cliente."""

    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="notes")
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.client.full_name} • Nota"


class ClientAnamnesisAnswer(models.Model):
    """Respostas por cliente, baseadas no builder."""

    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="anamnesis_answers")
    question = models.ForeignKey("anamnesis.AnamnesisQuestion", on_delete=models.CASCADE)
    value = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("client", "question")

    def __str__(self) -> str:
        return f"{self.client.full_name} • {self.question.title}"
