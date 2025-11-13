import os
import hikari
import lightbulb
import miru

from dotenv import load_dotenv
load_dotenv()

BOT: hikari.GatewayBot = hikari.GatewayBot(token=os.environ["TOKEN"], intents=hikari.Intents.ALL)
CLIENT: lightbulb.GatewayEnabledClient = lightbulb.client_from_app(BOT)
MIRU = miru.Client(BOT)