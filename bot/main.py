import os
import hikari
import lightbulb

from dotenv import load_dotenv
load_dotenv()

bot = hikari.GatewayBot(token=os.environ["TOKEN"])
client = lightbulb.client_from_app(bot)
bot.subscribe(hikari.StartingEvent, client.start)

@client.register
class Ping(
    lightbulb.SlashCommand,
    name="ding",
    description="Ping the bot",
):
    @lightbulb.invoke
    async def invoke(self, ctx: lightbulb.Context) -> None:
        print("Print")
        await ctx.respond("Pong!")
    
bot.run()