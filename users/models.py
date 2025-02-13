from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    STATUS_CHOICES = [
        ('thinking', 'Думает'),
        ('invited', 'Приглашен'),
    ]

    DIRECTION_CHOICES = [
        ('backend_python', 'Backend (Python)'),
        ('backend_js', 'Backend (JS)'),
        ('frontend', 'Frontend'),
        ('design', 'UI/UX Design'),
    ]


    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, unique=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='thinking')
    direction = models.CharField(max_length=20, choices=DIRECTION_CHOICES, blank=True, null=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Interview(models.Model):
    user = models.ForeignKey('UserProfile', on_delete=models.CASCADE)
    mentor = models.CharField(max_length=100)
    date_time = models.DateTimeField()
    whatsapp_number = models.CharField(max_length=20)

    def __str__(self):
        return f"Собеседование с {self.user.name} ({self.date_time})"