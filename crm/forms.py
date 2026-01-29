from django import forms
from .models import Client

class ClientForm(forms.ModelForm):
    """Form simples para o CRUD do cliente."""
    class Meta:
        model = Client
        fields = ["full_name","age","weight_kg","height_m","status","plan","last_activity_at"]
        widgets = {
            "last_activity_at": forms.DateInput(attrs={"type":"date"}),
        }
