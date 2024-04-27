from django.db import models
from user.models import Users
from django.utils import timezone

# Create your models here.

class   Room(models.Model):
    name = models.CharField(max_length=64)
    player1 = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='player1')
    player2 = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='player2', null=True, blank=True)
    is_active = models.BooleanField(default=False)  # Indicates if the game is currently active
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class   GameHistory(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE) 
    score_player1 = models.IntegerField()
    score_player2 = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

# class Game(models.Model):
#     room = models.OneToOneField(Room, on_delete=models.CASCADE, related_name='game')
#     player1 = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='player1')
#     player2 = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='player2')
#     paddle1_position = models.FloatField(default=0.5)
#     paddle2_position = models.FloatField(default=0.5)
#     ball_position_x = models.FloatField(default=0.5)
#     ball_position_y = models.FloatField(default=0.5)

#     def __str__(self):
#         return f"Game in Room {self.room.name}"

#     def update_paddle_position(self, user, position):
#         if user == self.player1:
#             self.paddle1_position = position
#         elif user == self.player2:
#             self.paddle2_position = position

#     def get_game_state(self):
#         return {
#             'paddle1_position': self.paddle1_position,
#             'paddle2_position': self.paddle2_position,
#             'ball_position_x': self.ball_position_x,
#             'ball_position_y': self.ball_position_y,
#         }