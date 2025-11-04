import os
import hikari
import lightbulb

from dotenv import load_dotenv
load_dotenv()

bot = hikari.GatewayBot(token=os.environ["TOKEN"], intents=hikari.Intents.ALL)
client = lightbulb.client_from_app(bot)
bot.subscribe(hikari.StartingEvent, client.start)

@client.register
class Ping(
    lightbulb.SlashCommand,
    name="ping",
    description="Ping the bot",
):
    @lightbulb.invoke
    async def invoke(self, ctx: lightbulb.Context) -> None:
        await ctx.respond("Pong!")

@client.register
class ReplaceRole(
    lightbulb.SlashCommand,
    name="replacerole",
    description="Find everybody who has a specific role, replace that role with another one.",
):
    
    roleA = lightbulb.role("role_a", "Find everybody with this role.")
    roleB = lightbulb.role("role_b", "Give them this role and remove the other one.")

    @lightbulb.invoke
    async def invoke(self, ctx: lightbulb.Context) -> None:
        await edit_role(self, ctx, remove=True)
        await ctx.respond("...", ephemeral=True)

@client.register
class AddRole(
    lightbulb.SlashCommand,
    name="addrole",
    description="Find everybody who has a specific role, give them another role.",
):
    
    roleA = lightbulb.role("role_a", "Find everybody with this role.")
    roleB = lightbulb.role("role_b", "Give them this role.")

    @lightbulb.invoke
    async def invoke(self, ctx: lightbulb.Context) -> None:
        await edit_role(self, ctx, remove=False)
        await ctx.respond("...", ephemeral=True)

async def edit_role(self, ctx: lightbulb.Context, remove: bool) -> None:
    guild = bot.cache.get_guild(os.environ["SERVER_ID"]) # type: ignore

    if guild is None:
        return
    
    members = guild.get_members()

    if members is None:
        return
    
    for member in members.values():
        if self.roleA not in member.get_roles():
            continue

        await member.add_role(self.roleB)

        if remove:
            await member.remove_role(self.roleA)

bot.run()