from enum import Enum

from django.utils.encoding import NoneType
from .player import Player
from random import uniform


class GameState(Enum):
    WAITING = "waiting"
    READY = "ready"
    PLAYING = "playing"


class Game:
    __BOARD_WIDTH = 512
    __BOARD_HEIGHT = 256
    __BALL_THICKNESS = 1
    __BALL_MIN_SPEED = 0.5
    __BALL_MAX_SPEED = 0.5

    def __init__(self, p1: Player | None = None, p2: Player | None = None) -> None:
        self.p1 = p1
        self.p2 = p2
        self.reset_board()
        if self.p1 is None or self.p2 is None:
            self.state = GameState.WAITING
        else:
            self.state = GameState.READY

    def ready(self) -> bool:
        return self.p1 is not None and self.p2 is not None

    def get_state(self) -> str:
        return self.state.value

    def p1_data(self) -> dict | None:
        if self.p1 is None:
            return None
        return self.p1.get_data()

    def p2_data(self) -> dict | None:
        if self.p2 is None:
            return None
        return self.p2.get_data()

    def update(self) -> None:
        if self.state != GameState.PLAYING:
            return
        if self.p1 is None or self.p2 is None:
            raise RuntimeError("Playing game with insuficient players")
        # ball-y
        # ball-x
        # player

        # Move vertically and check for colisions
        # TODO: Add thickness to calculations
        ball_new_pos_y = self.ball["pos"]["y"] + self.ball["movement"]["y"]
        ball_new_mov_y = self.ball["movement"]["y"]
        if ball_new_pos_y > self.__BOARD_HEIGHT / 2:
            ball_new_pos_y = (self.__BOARD_HEIGHT / 2) - (
                self.__BOARD_HEIGHT / 2 - ball_new_pos_y
            )
            ball_new_mov_y *= -1
        elif ball_new_pos_y < -self.__BOARD_HEIGHT / 2:
            ball_new_pos_y = -self.__BOARD_HEIGHT / 2 + (
                self.__BOARD_HEIGHT / 2 - ball_new_pos_y
            )
            ball_new_mov_y *= -1

        # Move horizontally and check for colisions
        ball_new_pos_x = self.ball["pos"]["x"] + self.ball["movement"]["x"]
        ball_new_mov_x = self.ball["movement"]["x"]
        if ball_new_pos_x + self.__BALL_THICKNESS / 2 >= self.__BOARD_WIDTH / 2:
            # This is a rough check using the old position. A proper calculation would be better
            if (
                self.p2.pos + self.p2.PADLE_HEIGHT / 2 < self.ball["pos"]["y"]
                or self.p2.pos - self.p2.PADLE_HEIGHT / 2 > self.ball["pos"]["y"]
            ):
                self.winner(self.p1)
                self.reset_board()
                return
            ball_new_pos_x = (self.__BOARD_WIDTH / 2 - self.__BALL_THICKNESS / 2) - (
                (ball_new_pos_x + self.__BALL_THICKNESS / 2) - self.__BOARD_WIDTH / 2
            )
            ball_new_mov_x *= uniform(-self.__BALL_MAX_SPEED, -self.__BALL_MIN_SPEED)
        elif ball_new_pos_x - self.__BALL_THICKNESS / 2 <= -self.__BOARD_WIDTH / 2:
            if (
                self.p1.pos + self.p1.PADLE_HEIGHT / 2 < self.ball["pos"]["y"]
                or self.p1.pos - self.p1.PADLE_HEIGHT / 2 > self.ball["pos"]["y"]
            ):
                self.winner(self.p2)
                self.reset_board()
                return
            ball_new_pos_x = -(self.__BOARD_WIDTH / 2 - self.__BALL_THICKNESS / 2) + (
                self.__BOARD_WIDTH / 2 - (ball_new_pos_x - self.__BALL_THICKNESS / 2)
            )
            ball_new_mov_x *= uniform(self.__BALL_MAX_SPEED, self.__BALL_MIN_SPEED)

        self.ball["pos"]["y"] = ball_new_pos_y
        self.ball["mov"]["y"] = ball_new_mov_y
        self.ball["pos"]["x"] = ball_new_pos_x
        self.ball["mov"]["x"] = ball_new_mov_x
        self.p1.update(self.__BOARD_HEIGHT)
        self.p2.update(self.__BOARD_HEIGHT)

    def start(self) -> None:
        self.ball["x"] = uniform(-self.__BALL_MAX_SPEED, self.__BALL_MAX_SPEED)
        self.ball["y"] = uniform(-self.__BALL_MAX_SPEED, self.__BALL_MAX_SPEED)

        # Set minimum speed to half speed
        if (
            self.ball["movement"]["x"] < 0
            and self.ball["movement"]["x"] > -self.__BALL_MIN_SPEED
        ):
            self.ball["movement"]["x"] -= self.__BALL_MIN_SPEED
        elif (
            self.ball["movement"]["x"] > 0
            and self.ball["movement"]["x"] < self.__BALL_MIN_SPEED
        ):
            self.ball["movement"]["x"] += self.__BALL_MIN_SPEED
        self.state = GameState.PLAYING

    def reset_board(self):
        self.ball = {"pos": {"x": 0, "y": 0}, "movement": {"x": 0.0, "y": 0.0}}

    def winner(self, p: Player):
        p.add_point()
