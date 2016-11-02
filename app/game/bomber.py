
import time

from app.game.input import Input, Command
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
        self.field = Field(11, 15, users)
        self.fetcher = Input(channel, self.reaction_handler)
        self.prev_tick = None
        self.chat_count = 0

    def start(self):
        self.running = True
        FieldOutputter.post_field(self.channel, self.field)
        self.prev_tick = time.time()
        while self.running:
            self.tick()
            time.sleep(0.5)

    def tick(self):
        tick_time = time.time()
        sec = tick_time - self.prev_tick
        self.field.proceed_time(sec)
        if self.should_send_as_new_message:
            FieldOutputter.post_field(self.channel, self.field, new_message=True)
            self.chat_count = 0
        else:
            FieldOutputter.post_field(self.channel, self.field)
        self.prev_tick = tick_time

    def reaction_handler(self, user, command):
        person = self.field.person_by_user(user)
        if person is None:
            return

        if command == Command.up:
            self.field.move_top(person)
        elif command == Command.right:
            self.field.move_right(person)
        elif command == Command.down:
            self.field.move_bottom(person)
        elif command == Command.left:
            self.field.move_left(person)
        elif command == Command.a:
            self.field.put_bomb(person)

    def add_chat_count(self):
        self.chat_count += 1

    @property
    def should_send_as_new_message(self):
        return self.chat_count >= 8

