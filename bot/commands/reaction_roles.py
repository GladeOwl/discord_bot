import logging
import hikari
import lightbulb

from hikari.errors import BadRequestError
from commands import perms
from core import CLIENT, BOT

LOGGER = logging.getLogger("bot")

@CLIENT.register
class CreateReactionRole(
    lightbulb.SlashCommand,
    name="createreactionrole",
    description="Create a message to give out roles based on reactions.",
    hooks=[perms.fail_if_not_officer]
):
    role: hikari.Role = lightbulb.role("role", "Role to give to whoever reacts to this message.")
    emoji: hikari.Emoji | str = lightbulb.string("emoji", "An emoji to use, default is :white_check_mark:.")
    channel: hikari.SnowflakeishOr = lightbulb.channel("channel", "The channel to post this message into.")
    message: str = lightbulb.string("description", "A description of the role.")

    @lightbulb.invoke
    async def invoke(self, ctx:lightbulb.Context) -> None:
        message: hikari.Message = await BOT.rest.create_message(self.channel, self.message)
        try:
            await message.add_reaction(self.emoji)
            await ctx.respond("Message was been posted.", ephemeral=True)
            logging.info(f"[Reaction Role] {self.role} was created in {self.channel} | By {ctx.member}")
        except BadRequestError:
            await ctx.respond("ERROR: Message was been posted but the bot couldn't react to the message, check if the Emoji is an Emoji. Please try again and delete the previous message.", ephemeral=True)
            logging.error(f"[Reaction Role] Failed to create. Role: {self.role} / Channel: {self.channel} / Emoji: {self.emoji} / Message: {self.message} | By {ctx.member}")
