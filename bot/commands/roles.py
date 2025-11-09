import hikari
import lightbulb
from typing import Mapping
from core import CLIENT

@CLIENT.register
class ReplaceRole(
    lightbulb.SlashCommand,
    name="replacerole",
    description="Find everybody who has role_a, and replace it with role_b.",
):
    
    roleA: hikari.Role = lightbulb.role("role_a", "Find everybody with this role.")
    roleB: hikari.Role  = lightbulb.role("role_b", "Give them this role and remove the other one.")

    @lightbulb.invoke
    async def invoke(self, ctx: lightbulb.Context) -> None:
        await edit_role(self.roleA, self.roleB, ctx, remove=True)
        await ctx.respond("...", ephemeral=True)

@CLIENT.register
class AddRole(
    lightbulb.SlashCommand,
    name="addrole",
    description="Find everybody who has a role_a, give them role_b.",
):
    roleA: hikari.Role = lightbulb.role("role_a", "Find everybody with this role.")
    roleB: hikari.Role = lightbulb.role("role_b", "Give them this role.")

    @lightbulb.invoke
    async def invoke(self, ctx: lightbulb.Context) -> None:
        await edit_role(self.roleA, self.roleB, ctx, remove=False)
        await ctx.respond("...", ephemeral=True)

async def edit_role(roleA, roleB, ctx: lightbulb.Context, remove: bool) -> None:
    member: hikari.Member | None = ctx.member
    print(member)
    if member is None:
        return
    
    guild: hikari.Guild | None = member.get_guild()
    print(guild)
    if guild is None:
        return
    
    members: Mapping[hikari.Snowflake, hikari.Member] = guild.get_members()
    if members is None:
        return
    
    for member in members.values():
        if roleA not in member.get_roles():
            continue

        await member.add_role(roleB)

        if remove:
            await member.remove_role(roleA)
