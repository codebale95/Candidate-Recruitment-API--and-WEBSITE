from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = [
        ('candidate', 'Candidate'),
        ('recruiter', 'Recruiter'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='candidate')

    def save(self, *args, **kwargs):
        # Set default role if not set
        if not self.role:
            self.role = 'candidate'
        super().save(*args, **kwargs)

class Candidate(models.Model):
    STAGE_CHOICES = [
        ('applied', 'Applied'),
        ('screening', 'Screening'),
        ('interview', 'Interview'),
        ('hired', 'Hired'),
        ('rejected', 'Rejected'),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=100)  # Job role they're applying for
    resume = models.TextField()
    stage = models.CharField(max_length=10, choices=STAGE_CHOICES, default='applied')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.email}"
