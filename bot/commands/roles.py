import logging
import hikari
import lightbulb

from typing import Mapping
from commands import perms
from core import CLIENT

LOGGER = logging.getLogger("bot")

@CLIENT.register
class ReplaceRole(
    lightbulb.SlashCommand,
    name="replacerole",
    description="Find everybody who has role_a, and replace it with role_b.",
    hooks=[perms.fail_if_not_officer]
):
    roleA: hikari.Role = lightbulb.role("role_a", "Find everybody with this role.")
    roleB: hikari.Role  = lightbulb.role("role_b", "Give them this role and remove the other one.")

    @lightbulb.invoke
    async def invoke(self, ctx: lightbulb.Context) -> None:
        await edit_role(self.roleA, self.roleB, ctx, remove=True)
        

@CLIENT.register
class AddRole(
    lightbulb.SlashCommand,
    name="addrole",
    description="Find everybody who has a role_a, also give them role_b.",
    hooks=[perms.fail_if_not_officer]
):
    roleA: hikari.Role = lightbulb.role("role_a", "Find everybody with this role.")
    roleB: hikari.Role = lightbulb.role("role_b", "Give them this role.")

    @lightbulb.invoke
    async def invoke(self, ctx: lightbulb.Context) -> None:
        await edit_role(self.roleA, self.roleB, ctx, remove=False)

async def edit_role(roleA, roleB, ctx: lightbulb.Context, remove: bool) -> None:
    member: hikari.Member | None = ctx.member
    if member is None:
        return
    
    guild: hikari.Guild | None = member.get_guild()
    if guild is None:
        return
    
    members: Mapping[hikari.Snowflake, hikari.Member] = guild.get_members()
    if members is None:
        return
    
    processed_members: int = 0
    members_with_role: int = 0
    for member in members.values():
        if roleA not in member.get_roles():
            continue
        
        if roleB not in member.get_roles():
            await member.add_role(roleB)
            processed_members += 1 if not remove else 0
        else:
            members_with_role += 1

        if remove:
            processed_members += 1
            await member.remove_role(roleA)

    if remove:
        message = f"By {ctx.member} : {roleA.mention} role was replaced with the {roleB.mention} role for {processed_members} member(s)."
        logging.info(message)
        await ctx.respond(message, ephemeral=True)
    else:
        message = f"By {ctx.member} : {roleB.mention} role was given to {processed_members} member(s) that also had the {roleA.mention} role."
        message = message + f" {members_with_role} member(s) already had the role." if members_with_role > 0 else ""
        logging.info(message)
        await ctx.respond(message, ephemeral=True)