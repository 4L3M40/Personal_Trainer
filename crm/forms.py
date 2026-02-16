from django import forms

from .models import Client, ClientFile, ClientNote


class ClientForm(forms.ModelForm):
    """Form simples para o CRUD do cliente."""

    class Meta:
        model = Client
        fields = ["full_name", "age", "weight_kg", "height_m", "status", "plan", "last_activity_at"]
        widgets = {
            "last_activity_at": forms.DateInput(attrs={"type": "date"}),
        }


class ClientFileForm(forms.ModelForm):
    class Meta:
        model = ClientFile
        fields = ["title", "file"]


class ClientNoteForm(forms.ModelForm):
    class Meta:
        model = ClientNote
        fields = ["text"]
        widgets = {
            "text": forms.Textarea(attrs={"rows": 4}),
        }
