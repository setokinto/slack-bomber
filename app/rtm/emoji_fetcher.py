
import json

from slacker import Slacker
from websocket import WebSocketApp
from slackbot_settings import API_TOKEN

_fetchers = {}

class EmojiFetcher:

    def __init__(self, target_channel_id, handler):
        self.target_channel_id = target_channel_id
        self.handler = handler
        _fetchers[target_channel_id] = self


def fire_emoji_fetcher(user, reaction, channel, fetchers = None):
    if fetchers is None:
        fetchers = _fetchers

    if channel in fetchers:
        fetchers[channel].handler(user, reaction, channel)

def get_content_from_message(message):
    if message["type"] == "reaction_removed" or message["type"] == "reaction_added":
        user = message["user"]
        reaction = message["reaction"]
        channel = message["item"]["channel"]

        return {
            "user": user,
            "reaction": reaction,
            "channel": channel,
        }
    return None

def on_message(ws, message):
    message = json.loads(message)
    content = get_content_from_message(message)
    if content is not None:
        fire_emoji_fetcher(content["user"], content["reaction"], content["channel"])

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    print("### opened ###")

connected = False
def connect():
    global connected
    if connected:
        return
    connected = True
    slacker = Slacker(API_TOKEN)
    url = slacker.rtm.start().body["url"]
    ws = WebSocketApp(url,
                      on_message = on_message,
                      on_error = on_error,
                      on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()

