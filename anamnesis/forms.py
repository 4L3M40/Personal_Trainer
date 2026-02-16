from django import forms
from .models import AnamnesisQuestion

class QuestionForm(forms.ModelForm):
    class Meta:
        model = AnamnesisQuestion
        fields = ["title","field_type","options"]
