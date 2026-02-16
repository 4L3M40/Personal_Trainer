from django import forms

from .models import ProgressRecord


class ProgressRecordForm(forms.ModelForm):
    class Meta:
        model = ProgressRecord
        fields = ["date", "weight_kg", "notes"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
        }
