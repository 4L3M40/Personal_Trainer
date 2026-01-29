from django.db import models

class AnamnesisQuestion(models.Model):
    """Perguntas configuráveis do questionário (builder)."""

    class FieldType(models.TextChoices):
        TEXT = "text", "text"
        SELECT = "select", "select"
        RADIO = "radio", "radio"

    title = models.CharField(max_length=180)
    field_type = models.CharField(max_length=12, choices=FieldType.choices, default=FieldType.TEXT)
    options = models.CharField(max_length=400, blank=True, help_text="Para select/radio: opções separadas por ';'")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title
