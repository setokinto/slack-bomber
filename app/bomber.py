
import re

from slackbot.bot import respond_to, listen_to

from app.game.bomber import BomberFactory


@respond_to("start with (.*)")
def start(message, who):
    users = set(re.findall("<@([\w]*)>", who))
    users.add(message.body["user"])

    if len(users) <= 1:
        message.reply("bomber is not started because user not found.")
        return

    message.reply("slack-bomber is started:")
    BomberFactory.create(message.body["channel"], list(users))

@respond_to("stop|quit|finish|end|bye")
def end(message):
    BomberFactory.remove(message.body["channel"])
    message.reply("finished")

@listen_to(".*")
def any(message):
    bomber = BomberFactory.instance(message.body["channel"])
    if bomber is not None:
        bomber.add_chat_count()

