import lightbulb
from core import CLIENT

@CLIENT.register
class Ping(
    lightbulb.SlashCommand,
    name="ping",
    description="Ping the bot",
):
    @lightbulb.invoke
    async def invoke(self, ctx: lightbulb.Context) -> None:
        await ctx.respond("Pong!")