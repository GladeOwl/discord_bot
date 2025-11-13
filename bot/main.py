import hikari
import logging


from core import BOT, CLIENT
from commands import *
from modules import *

LOGGER = logging.getLogger()
file_handler = logging.FileHandler("./bot.log", encoding="utf-8")
formatter = logging.Formatter("[%(asctime)s] (%(filename)s) %(levelname)s :: %(message)s")
file_handler.setFormatter(formatter)
LOGGER.addHandler(file_handler)

BOT.subscribe(hikari.StartingEvent, CLIENT.start)
BOT.run()