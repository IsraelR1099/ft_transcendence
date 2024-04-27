import threading

from channels.consumer import async_to_sync
from pong.game.game import Game
from channels.generic.websocket import JsonWebsocketConsumer


class Rooms(JsonWebsocketConsumer):
    rooms = {}

    ########################
    # General room methods #
    ########################

    @classmethod
    def get_room_data(cls, room_name: str, room: dict) -> dict:
        return {
            "name": room_name,
            "spectators": room["spectators"],
            "players": {
                "p1": room["game"].p1_data(),
                "p2": room["game"].p2_data(),
            },
            "status": room["game"].get_state(),
        }

    @classmethod
    def get_rooms(cls) -> list:
        room_list = []
        for name, room in cls.rooms.items():
            room_list.append(cls.get_room_data(name, room))
        return room_list

    def get_room(self, room_name: str) -> dict:
        if room_name in self.rooms:
            return self.rooms[room_name]
        self.rooms[room_name] = {
            "game": Game(),
            "thread": threading.Thread(
                target=self.update, kwargs={"room_name": room_name}
            ),
            "players": 0,
            "spectators": 0,
            "active": True,
        }
        return Rooms.rooms[room_name]

    def rem_room(self, room_name: str) -> None:
        if room_name not in self.rooms:
            return
        del self.rooms[room_name]

    #################
    # Communication #
    #################

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def connect(self) -> None:
        name = "..."  # TODO: Parse query string
        self.room = self.get_room(name)
        if "participants" not in self.room:
            self.room["participants"] = [self]
        else:
            self.room["participants"].append(self)
        player = True  # TODO: Parse query string
        if player:  # TODO: Check if there is space. Fail connection if there isn't
            self.room["player"] += 1
            self.player = True
        else:
            self.room["spectators"] += 1
            self.player = False
        return super().connect()

    @classmethod
    def update(cls, room_name):
        while room_name in cls.rooms and cls.rooms[room_name]["active"]:
            room = cls.rooms[room_name]
            async_to_sync(room["participants"][0].channel_layer.group_send)(
                room_name,
                {"type": "stream_state", "state": room},
            )
            pass
