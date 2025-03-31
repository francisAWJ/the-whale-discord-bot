import discord
from discord.ext import commands

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='join', help="Join a voice channel")
    async def join(self, ctx):
        try:
            voice_channel = ctx.message.author.voice.channel

            if ctx.voice_client is not None:
                return await ctx.voice_client.move_to(voice_channel)
            
            await voice_channel.connect()
            await ctx.send(f"i have joined **{voice_channel.name}**...")
        except Exception as err:
            await ctx.send(f"**ERORR**: {err}")

    @commands.command(name='leave', help="Leave the voice channel")
    async def leave(self, ctx):
        await ctx.send(f"i have left **{ctx.voice_client.channel}**...")
        await ctx.voice_client.disconnect()
