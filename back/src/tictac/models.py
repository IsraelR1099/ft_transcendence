from django.db import models


class Game(models.Model):
    room_code = models.CharField(max_length=4, unique=True)
    creator = models.CharField(max_length=50)
    opponent = models.CharField(max_length=50, blank=True, null=True)
    is_over = models.BooleanField(default=False)

