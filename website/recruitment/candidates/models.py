from django.db import models
from django.contrib.auth.models import User

class Candidate(models.Model):
    STATUS_CHOICES = [
        ('APPLIED', 'Applied'),
        ('SCREENING', 'Screening'),
        ('INTERVIEW', 'Interview'),
        ('HIRED', 'Hired'),
        ('REJECTED', 'Rejected'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    role = models.CharField(max_length=100)
    resume_text = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='APPLIED')

    def __str__(self):
        return f"{self.name} - {self.status}"
