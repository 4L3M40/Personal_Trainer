from django.contrib import admin
from .models import Appointment, Feedback, Alert

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ("title","client","starts_at","ends_at")
    list_filter = ("starts_at",)
    search_fields = ("title","client__full_name")

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ("client","created_at")
    search_fields = ("client__full_name","text")

@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ("title","is_open","created_at")
    list_filter = ("is_open",)
