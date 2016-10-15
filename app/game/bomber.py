
from app.game.input import Input
from app.slack import slacker

class BomberFactory:
    _bomber_store = {}

    @classmethod
    def create(cls, channel, users):
        bomber = cls.instance(channel)
        if bomber is None:
            bomber = Bomber(channel, users)
            cls._bomber_store[channel] = bomber

        return bomber

    @classmethod
    def instance(cls, channel):
        if channel in cls._bomber_store:
            return cls._bomber_store[channel]
        return None

class Bomber:

    def __init__(self, channel, users):
        self.channel = channel
        self.users = users
        self.field = []
        self.fetcher = Input(channel, self.reaction_handler)

    def reaction_handler(self, user, command):
        slacker.chat.post_message(self.channel, user +": " + str(command))
