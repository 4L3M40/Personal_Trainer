from django.contrib import admin
from .models import Client, Plan

@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    search_fields = ("name",)

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("full_name", "status", "plan", "last_activity_at")
    list_filter = ("status", "plan")
    search_fields = ("full_name",)
