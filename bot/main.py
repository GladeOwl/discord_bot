import hikari

from core import BOT, CLIENT
from commands import *

BOT.subscribe(hikari.StartingEvent, CLIENT.start)
BOT.run()