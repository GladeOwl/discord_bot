import hikari
import lightbulb
from lightbulb.prefab import checks

from core import CLIENT

@lightbulb.hook(lightbulb.ExecutionSteps.CHECKS)
async def fail_if_not_officer(_:lightbulb.ExecutionPipeline, ctx: lightbulb.Context) -> None:
    member: hikari.Member | None = ctx.member
    
    if member is None:
        return
    
    if hikari.Permissions.ADMINISTRATOR not in member.permissions:
        await ctx.respond("You lack the required permissions to execute this command. Please ding an Officer for help.", ephemeral=True)
        raise lightbulb.prefab.checks.MissingRequiredPermission # pyright: ignore[reportAttributeAccessIssue]