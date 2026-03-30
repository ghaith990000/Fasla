from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class GameSession(models.Model):
    MODE_CHOICES = [
        ("individual", "Individual"),
        ("team", "Team"),
    ]

    STATUS_CHOICES = [
        ("waiting", "Waiting"),
        ("in_progress", "In Progress"),
        ("finished", "Finished"),
    ]

    host = models.ForeignKey(User, on_delete=models.CASCADE)
    mode = models.CharField(max_length=20, choices=MODE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="waiting")

    config = models.JSONField(default=dict)  # Store game configuration as JSON

    created_at = models.DateTimeField(auto_now_add=True)
    started_at = models.DateTimeField(null=True, blank=True)
    ended_at = models.DateTimeField(null=True, blank=True)

class Team(models.Model):
    session = models.ForeignKey(GameSession, on_delete=models.CASCADE, related_name='teams')
    name = models.CharField(max_length=100)
    score = models.IntegerField(default=0)

class Player(models.Model):
    session = models.ForeignKey(GameSession, on_delete=models.CASCADE, related_name='players')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, null=True, blank=True, on_delete=models.SET_NULL)
    score = models.IntegerField(default=0)
    joined_at = models.DateTimeField(auto_now_add=True)

class GameTurn(models.Model):
    session = models.ForeignKey(GameSession, on_delete=models.CASCADE, related_name='turns')
    current_player = models.ForeignKey(Player, null=True, blank=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)