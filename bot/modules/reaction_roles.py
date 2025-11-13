import logging
import hikari
import miru

from modules import helper
from core import BOT, MIRU

LOGGER = logging.getLogger("bot")
DATA_FILE : str = "reaction_roles.json"


class ReactionRoleButtonView(miru.View):
    def __init__(self, role: hikari.Role, add_message: str, remove_message: str):
        super().__init__(timeout=None)
        self.role: hikari.Role = role
        self.add_message: str = add_message
        self.remove_message: str = remove_message
    
        btn = miru.Button(
            label="Add/Remove Role",
            custom_id=str(self.role.id)
        )
        btn.callback = self.button
        self.add_item(btn)

    async def button(self, ctx: miru.ViewContext) -> None:

        guild: hikari.GatewayGuild | None = ctx.get_guild()
        if guild is None:
            logging.error("[Reaction Role / miru] Unable to find guild.")
            return
        
        member: hikari.Member | None = guild.get_member(ctx.user)
        if member is None:
            logging.error("[Reaction Role / miru] Unable to find member.")
            return
        
        if self.role not in member.get_roles():
            await member.add_role(self.role)
            await ctx.respond(self.add_message, flags=hikari.MessageFlag.EPHEMERAL)
            logging.info(f"[Reaction Role] {member} has taken the {self.role} role.")
        else:
            await member.remove_role(self.role)
            await ctx.respond(self.remove_message, flags=hikari.MessageFlag.EPHEMERAL)
            logging.info(f"[Reaction Role] {member} has removed the {self.role} role.")
    
    def save_local_data(self, message: hikari.Message) -> None:
        data: dict = {
            "guild_id": self.role.guild_id,
            "channel_id": message.channel_id,
            "message_id": message.id,
            "role_id": self.role.id,
            "add_message": self.add_message,
            "remove_message": self.remove_message
        }

        helper.write_to_json_list(DATA_FILE, data)
        

@BOT.listen()
async def start_views(event: hikari.StartedEvent) -> None:
    data: list[dict] | None = helper.read_json_list(DATA_FILE)
    if data is None:
        logging.error(f"No data was able to be retrieved for Miru Views. Peristence failed.")
        return
    
    processed_views: int = 0
    for item in data:
        role : hikari.Role = await BOT.rest.fetch_role(item["guild_id"], item["role_id"])
        view = ReactionRoleButtonView(role=role, add_message=item["add_message"], remove_message=item["remove_message"])
        MIRU.start_view(view, bind_to=item["message_id"])
        processed_views += 1
    
    logging.info(f"[Reaction Role / miru] {processed_views} views were made persistent.")