import discord
from discord.ext import commands
import os

from help_cog import help_cog
from music_cog import music_cog

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="/", intents=intents)
# Eliminamos el comando help por defecto
bot.remove_command("help")

async def load_cogs(bot):
    await bot.wait_until_ready()
    await bot.add_cog(help_cog(bot))
    await bot.add_cog(music_cog(bot))

@bot.event
async def on_papu():
    print(f'Logged in as {bot.user.name} - {bot.user.id}\n')
    print(f'Successfully connected to Discord\n')
    await load_cogs(bot)
# Iniciamos el bot
bot.run("MTEwNDk4OTA1Njc0OTgxMzc5MQ.GL7p0s.i1PxmGE-ovEvFDlkICt-WOP7GwgAwkhMGEADZY")
