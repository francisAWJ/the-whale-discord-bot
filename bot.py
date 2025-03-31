import os
import discord
import asyncio

from dotenv import load_dotenv
from discord.ext import commands
from cogs.scraper import Scraper
from cogs.music import Music
from cogs.misc import Misc

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents().default()
intents.message_content = True

bot = commands.Bot(command_prefix='..', 
                   description='the WHALE‼️‼️‼️🐳🐳🐳', 
                   intents=intents)

@bot.command(name='reload', help='Reloads the command')
@commands.is_owner()
async def reload(ctx, extension):
    await bot.reload_extension(f"cogs.{extension}")
    embed = discord.Embed(title='Reload', description=f'{extension} successfully reloaded', color=0xff00c8)
    await ctx.send(embed=embed)

@bot.event
async def on_ready():
    print(f"{bot.user.name} has connected to Discord!")

async def main():
    async with bot:
        await bot.add_cog(Scraper(bot))
        await bot.add_cog(Music(bot))
        await bot.add_cog(Misc(bot))
        
        await bot.start(TOKEN)

asyncio.run(main())
