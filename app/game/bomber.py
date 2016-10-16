
import time

from app.game.input import Input
from app.game.field import Field
from app.game.field_outputter import FieldOutputter
from app.slack import slacker

class BomberFactory:
    _bomber_store = {}

    @classmethod
    def create(cls, channel, users):
        bomber = cls.instance(channel)
        if bomber is None:
            bomber = Bomber(channel, users)
            cls._bomber_store[channel] = bomber
            bomber.start()

        return bomber

    @classmethod
    def remove(cls, channel):
        cls._bomber_store[channel].running = False
        del cls._bomber_store[channel]


    @classmethod
    def instance(cls, channel):
        if channel in cls._bomber_store:
            return cls._bomber_store[channel]
        return None

class Bomber:

    def __init__(self, channel, users):
        self.channel = channel
        self.users = users
        self.field = Field(8, 10, users)
        self.fetcher = Input(channel, self.reaction_handler)

    def start(self):
        self.running = True
        while self.running:
            self.tick()
            time.sleep(1)

    def tick(self):
        FieldOutputter.post_field(self.channel, self.field)

    def reaction_handler(self, user, command):
        slacker.chat.post_message(self.channel, user +": " + str(command))

