from django.db import models
from django.contrib.auth.models import User  # Import the User model
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    due_date = models.DateField(blank=True, null=True)
    priority = models.CharField(
        max_length=10,
        choices=[('High', 'High'), ('Medium', 'Medium'), ('Low', 'Low')],
        default='Medium'
    )
    completed = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')  # Link task to a specific user

    def __str__(self):
        return self.title
