from django.db import models

class Exercise(models.Model):
    """Exercício cadastrado na biblioteca."""
    name = models.CharField(max_length=120)
    muscle_group = models.CharField(max_length=80, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self) -> str:
        return self.name

class Food(models.Model):
    """Alimento com macros por porção padrão (ex.: 100g, 30g)."""
    name = models.CharField(max_length=160)
    portion_label = models.CharField(max_length=40, default="100g")
    kcal = models.PositiveIntegerField(default=0)
    protein_g = models.DecimalField(max_digits=5, decimal_places=1, default=0)
    carbs_g = models.DecimalField(max_digits=5, decimal_places=1, default=0)
    fats_g = models.DecimalField(max_digits=5, decimal_places=1, default=0)

    def __str__(self) -> str:
        return f"{self.name} ({self.portion_label})"
