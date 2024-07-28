from django.db import models
from django.utils import timezone
from common_app.models import User

class GameRound(models.Model):
    round_number = models.IntegerField()
    correct_color = models.CharField(max_length=10)
    end_time = models.DateTimeField()

    def __str__(self):
        return f"Round {self.round_number} - {self.correct_color}"

    def is_active(self):
        return timezone.now() < self.end_time

class UserPrediction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game_round = models.ForeignKey(GameRound, on_delete=models.CASCADE)
    predicted_color = models.CharField(max_length=10)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.full_name} - {self.predicted_color} (Round {self.game_round.round_number})"
