from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

import json
import logging


class GameRoom(WebsocketConsumer):
    def connect(self):
        try:
            # Build a channel group for each room_code. We retrieve the
            # room_code from the URL.
            self.room_name = self.scope['url_route']['kwargs']['room_code']
            self.room_group_name = 'room_%s' % self.room_name
            print(self.room_group_name)

            # Join room group
            async_to_sync(self.channel_layer.group_add)(
                    self.room_group_name,
                    self.channel_name
            )

            self.accept()
        except Exception as e:
            logging.error(f"Error connecting to websocket: {e}")

    def disconnect(self):
        try:
            async_to_sync(self.channel_layer.group_discard)(
                    self.room_group_name,
                    self.channel_name
            )
        except Exception as e:
            logging.error(f"Error disconnecting from websocket: {e}")

    def receive(self, text_data):
        try:
            # When you receive a message from the Websocket connection, instead
            # of sending the message to the associated channel, you send to the
            # group. We use group_send() method of the channel layer. We pass
            # type which invokes a method that receives the event. It executes
            # every time a message with that specific type is received
            print(text_data)
            async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name, {
                        'type': 'run_game',
                        'payload': text_data
                    }
            )
        except Exception as e:
            logging.error(f"Error receiving message from websocket: {e}")

    def run_game(self, event):
        # When a message with type run_game is sent to the group, all consumers
        # subscribed to the group will receive the message and will execute the
        # run_game() method
        data = event['payload']
        data = json.loads(data)

        self.send(text_data=json.dumps({
            'payload': data['data']
            }))
