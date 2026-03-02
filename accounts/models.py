from django.conf import settings
from django.db import models
from crm.models import Client


class PersonalProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="personal_profile",
    )

    def __str__(self):
        return f"Personal: {self.user.username}"


class StudentProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="student_profile",
    )
    client = models.OneToOneField(
        Client,
        on_delete=models.CASCADE,
        related_name="student_profile",
    )
    personal = models.ForeignKey(
        PersonalProfile,
        on_delete=models.CASCADE,
        related_name="students",
    )

    def __str__(self):
        return f"Student: {self.user.username} (client_id={self.client_id})"