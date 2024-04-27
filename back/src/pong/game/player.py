from enum import Enum


class Direction(Enum):
    UP = 1
    DOWN = -1


class Player:
    PADLE_HEIGHT = 28

    def __init__(self, user) -> None:
        self.user = user
        self.pos = 0
        self.points = 0

    def move(self, dir: Direction) -> None:
        self.moving = True
        self.move_dir = dir

    def stop(self) -> None:
        self.moving = False

    def update(self, court_height: int) -> None:
        actual_height = court_height / 2 - self.PADLE_HEIGHT / 2
        if (
            self.pos + self.move_dir.value <= actual_height
            and self.pos + self.move_dir.value >= -court_height
        ):
            self.pos += self.move_dir.value

    def add_point(self, points: int = 1):
        self.points += points

    def get_data(self) -> dict:
        return {
            "position": self.pos,
            "points": self.points,
            "paddle_height": self.PADLE_HEIGHT,
        }
