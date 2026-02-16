from django.contrib import admin
from .models import AnamnesisQuestion

@admin.register(AnamnesisQuestion)
class AnamnesisQuestionAdmin(admin.ModelAdmin):
    list_display = ("title","field_type","created_at")
    search_fields = ("title",)
