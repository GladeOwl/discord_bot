import logging
import hikari
import lightbulb
from typing import Optional

from modules.reaction_roles import ReactionRoleButtonView
from commands import perms
from core import CLIENT, BOT, MIRU

LOGGER = logging.getLogger("bot")

@CLIENT.register
class CreateReactionRole(
    lightbulb.SlashCommand,
    name="createreactionrole",
    description="Create a message to give out roles on a button click.",
    hooks=[perms.fail_if_not_officer]
):
    role: hikari.Role = lightbulb.role("role", "Role to give to whoever reacts to this message.")
    channel: hikari.SnowflakeishOr = lightbulb.channel("channel", "The channel to post this message into.")
    description: str = lightbulb.string("description", "A description of the role.")
    footer: Optional[str] = lightbulb.string("footer", "Extra bit of text as a Warning or Advisory for the role.", default=None)
    role_add_message: str = lightbulb.string("role_add_message", "This message is sent to the user upon getting the role.", default="Role added.")
    role_remove_message: str = lightbulb.string("role_remove_message", "This message is sent to the user upon removing the role.", default="Role removed.")
    
    @lightbulb.invoke
    async def invoke(self, ctx:lightbulb.Context) -> None:
        embed: hikari.Embed = hikari.Embed(
            title=self.role.name,
            description=self.description,
        )

        if self.footer:
            embed.set_footer(self.footer)

        view = ReactionRoleButtonView(self.role, self.role_add_message, self.role_remove_message)
        message: hikari.Message = await BOT.rest.create_message(self.channel, embed=embed, components=view)
        view.save_local_data(message)
        MIRU.start_view(view)

        await ctx.respond("Message was been posted.", ephemeral=True)
        logging.info(f"[Reaction Role] {self.role} was created in {self.channel} | By {ctx.member}")