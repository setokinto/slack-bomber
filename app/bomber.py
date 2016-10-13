
from slackbot.bot import respond_to

@respond_to("start with (.*)")
def start(message, who):
    message.reply("Yeah! Start bomber!!")

