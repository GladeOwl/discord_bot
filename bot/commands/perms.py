import logging
import hikari
import lightbulb

LOGGER = logging.getLogger("bot")

@lightbulb.hook(lightbulb.ExecutionSteps.CHECKS)
async def fail_if_not_officer(_:lightbulb.ExecutionPipeline, ctx: lightbulb.Context) -> None:
    member: hikari.Member | None = ctx.member
    
    if member is None:
        return
    
    if hikari.Permissions.ADMINISTRATOR not in member.permissions:
        logging.info(f"{ctx.member} tried to use the command {ctx.command}, but lacked the appropriate roles.")
        await ctx.respond("You lack the required permissions to execute this command. Please ding an Officer for help.", ephemeral=True)
        raise lightbulb.prefab.checks.MissingRequiredPermission # pyright: ignore[reportAttributeAccessIssue]