from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# models.py
from django.db import models
from django.contrib.auth.models import User

class VolunteerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total_hours = models.IntegerField(default=0)
    rank = models.PositiveIntegerField(default=0)
    
    
    def __str__(self):
        return f"{self.user.username} - {self.total_hours} hours"

class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    hours_reward = models.IntegerField(default=0)
    max_participants = models.IntegerField(default=1)  
    is_completed = models.BooleanField(default=False)
    current_participants = models.ManyToManyField(User, related_name='tasks', blank=True)  # Users who have taken the task

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Reward(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    required_hours = models.PositiveIntegerField()
    granted_to = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return self.title


# Create your models here.
