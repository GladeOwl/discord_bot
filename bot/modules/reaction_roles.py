import logging
import hikari
import lightbulb
import miru
from core import BOT, CLIENT, MIRU

LOGGER = logging.getLogger("bot")

class ReactionRoleButtonView(miru.View):
    def __init__(self, role: hikari.Role, add_message: str, remove_message: str):
        super().__init__(timeout=None)
        self.role: hikari.Role = role
        self.add_message: str = add_message
        self.remove_message: str = remove_message

        self.add_item(
            miru.Button(
                label="Add/Remove Role",
                style=hikari.ButtonStyle.PRIMARY,
                custom_id=f"reaction_role:{self.role.id}"
            )
        )

    async def button(self, ctx: miru.ViewContext, button: miru.Button) -> None:
        guild: hikari.GatewayGuild | None = ctx.get_guild()
        if guild is None:
            logging.error("[ReactionRoleButtonView] Unable to find guild.")
            return
        
        member: hikari.Member | None = guild.get_member(ctx.user)
        if member is None:
            logging.error("[ReactionRoleButtonView] Unable to find member.")
            return
        
        if self.role not in member.get_roles():
            await member.add_role(self.role)
            await ctx.respond(self.add_message, flags=hikari.MessageFlag.EPHEMERAL)
        else:
            await member.remove_role(self.role)
            await ctx.respond(self.remove_message, flags=hikari.MessageFlag.EPHEMERAL)
