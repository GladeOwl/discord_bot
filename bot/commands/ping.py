import logging
import lightbulb
from core import CLIENT

LOGGER = logging.getLogger("bot")

@CLIENT.register
class Ping(
    lightbulb.SlashCommand,
    name="ping",
    description="Ping the bot"
):
    @lightbulb.invoke
    async def invoke(self, ctx: lightbulb.Context) -> None:
        logging.info(f"By {ctx.member} : Ping!")
        await ctx.respond("Pong!", ephemeral=True)