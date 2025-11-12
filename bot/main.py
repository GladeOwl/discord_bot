import hikari
import logging

from core import BOT, CLIENT
from commands import *

LOGGER = logging.getLogger("bot")
logging.basicConfig(
    filename="./bot.log",
    encoding="utf-8",
    level=logging.INFO,
    format="[%(asctime)s] (%(filename)s) %(levelname)s :: %(message)s",  
)

BOT.subscribe(hikari.StartingEvent, CLIENT.start)
BOT.run()