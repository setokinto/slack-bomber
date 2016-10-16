
from slackbot.bot import respond_to

from app.rtm.emoji_fetcher import connect
from app.game.bomber import BomberFactory


@respond_to("start with (.*)")
def start(message, who):
    message.reply("Yeah! Start bomber!!")
    BomberFactory.create(message.body["channel"], [
      "user1"
    ])

    connect() # FIXME: this connect may be block a thread

@respond_to("stop|quit|finish|end|bye")
def end(message):
    BomberFactory.remove(message.body["channel"])
    message.reply("finished")

