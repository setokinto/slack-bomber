
import threading

from slackbot.bot import Bot
from app.rtm.emoji_fetcher import connect
import app

def main():
    rtm_reaction_loop = threading.Thread(target=connect)
    rtm_reaction_loop.start()

    bot = Bot()
    bot.run()


if __name__ == "__main__":
    main()

