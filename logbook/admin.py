from django.contrib import admin
from .models import ProgressRecord

@admin.register(ProgressRecord)
class ProgressRecordAdmin(admin.ModelAdmin):
    list_display = ("client","date","weight_kg")
    list_filter = ("date",)
    search_fields = ("client__full_name",)
