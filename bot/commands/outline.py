import logging
import os

import hikari
import lightbulb
import requests

from modules import helper
from core import CLIENT, BOT
from dotenv import load_dotenv

from commands import perms

load_dotenv()

LOGGER = logging.getLogger("bot")

@CLIENT.register
class ScanOutlineGroups (
    lightbulb.SlashCommand,
    name="scanoutlinegroups",
    description="Force a manual scan.",
    hooks=[perms.fail_if_not_officer]
):
    async def contact_api(self, http: str, endpoint: str, data: dict = {}) -> dict:
        url: str = f"{os.environ['OUTLINE_URL']}{endpoint}"
        headers = {
            "Authorization": f"Bearer {os.environ['OUTLINE_API_KEY']}", 
            "accept": "application/json", 
            "content-type": "application/json"
        }

        response: requests.Response = requests.request(http, url, json=data, headers=headers)
        
        if response.status_code != 200:
            reply: dict = response.json()
            logging.error(f"API HTTP Error; {response.status_code}. Error: {reply['error']} | {reply['message']}")
        return response.json()

    async def get_members(self, ctx: lightbulb.Context) -> list:
        data: list = await self.contact_api("POST", "users.list")

        members = []
        guild_members = {}
        
        guild_members_data = BOT.cache.get_guild(ctx.guild_id).get_members()
        for userId, member in guild_members_data.items():
            guild_members[member.username.lower()] = member

        for item in data["data"]:
            try:
                member: hikari.guilds.Member = guild_members[item["name"].lower()]
                members.append({ "name": item["name"], "outlineId": item["id"],  "discordId": member.id, "roles": member.role_ids})
            except KeyError:
                await helper.create_ctx_error(ctx, f"User: {item['name']} not found. Please confirm if their Discord and Outline usernames are the same.")
                return None
                
        return members

    async def get_groups_and_roles(self, members: list, ctx: lightbulb.Context) -> dict:
        data: dict = await self.contact_api("POST", "groups.list")
        groups_and_roles: dict = {}
        guild_roles = {}

        guild_roles_data = BOT.cache.get_guild(ctx.guild_id).get_roles()
        for roleId, role in guild_roles_data.items():
            guild_roles[role.name.lower()] = roleId
        
        for item in data["data"]["groups"]:
            try:
                role: str = guild_roles[item["name"].lower()]
                groups_and_roles[item["name"]] = {"groupId": item["id"], "roleId": role}
            except KeyError:
                await helper.create_ctx_error(ctx, f"Role: {item['name']} cannot be found. Skipping")
                continue
        
        print(groups_and_roles.items())
        return groups_and_roles

    async def add_to_groups(self, members: list, groups_and_roles: dict) -> None:
        for member in members:
            for group_name, ids in groups_and_roles.items():
                if ids["roleId"] in member["roles"]:
                    data = {
                        "id": ids["groupId"],
                        "userId": member["outlineId"]
                    }
                    await self.contact_api("POST", "groups.add_user", data=data)
                    logging.info(f"{member['name']} was added to the {group_name} group.")

    @lightbulb.invoke
    async def invoke(self, ctx: lightbulb.Context) -> None:
        has_error: bool = False

        members: list = await self.get_members(ctx)
        if members is None:
            has_error = True

        groups_and_roles: dict = await self.get_groups_and_roles(members, ctx)
        if groups_and_roles is None:
            has_error = True

        await self.add_to_groups(members, groups_and_roles)

        if not has_error:
            await ctx.respond("Manual Scan Initiated. Please check Outline for any changes.", ephemeral=True)