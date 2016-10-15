
from slackbot.bot import respond_to

from app.rtm.emoji_fetcher import EmojiFetcher, connect

@respond_to("start with (.*)")
def start(message, who):
    connect()
    message.reply("Yeah! Start bomber!!")

