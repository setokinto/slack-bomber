
from slackbot.bot import respond_to

from app.rtm.emoji_fetcher import connect
from app.game.bomber import BomberFactory


@respond_to("start with (.*)")
def start(message, who):
    message.reply("Yeah! Start bomber!!")

    connect()
    BomberFactory.create(message.body["channel"], [
      "user1"
    ])


