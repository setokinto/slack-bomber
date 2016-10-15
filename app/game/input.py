
from enum import Enum

from app.rtm.emoji_fetcher import EmojiFetcher

class Command(Enum):
    up = 0
    right = 1
    down = 2
    left = 3
    a = 4

    @staticmethod
    def reaction_to_command(reaction):
        _mapper = {
            "arrow_left": Command.left,
            "arrow_up": Command.up,
            "arrow_down": Command.down,
            "arrow_right": Command.right,
            "a": Command.a,
        }
        if reaction in _mapper:
            return _mapper[reaction]
        return None

class Input:

    def __init__(self, channel, handler):
        self.channel = channel
        self._handler = handler
        self._fetcher = EmojiFetcher(channel, self._fetcher_handler)

    def _fetcher_handler(self, user, reaction, channel):
        command = Command.reaction_to_command(reaction)
        if command is not None:
            self._handler(user, command)

