from django.db import models
from games.models import GameSession, Player
from questions.models import Question, Answer

# Create your models here.
class GameBoard(models.Model):
    session = models.OneToOneField(GameSession, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class BoardCell(models.Model):
    board = models.ForeignKey(GameBoard, on_delete=models.CASCADE, related_name="cells")
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    row = models.IntegerField()
    column = models.IntegerField()
    points = models.IntegerField(default=100)

    is_answered = models.BooleanField(default=False)

class PlayerResponse(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    cell = models.ForeignKey(BoardCell, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)

    is_correct = models.BooleanField()
    response_time_ms = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
