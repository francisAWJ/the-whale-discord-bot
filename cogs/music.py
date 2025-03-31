import asyncio
import discord
import yt_dlp

from discord.ext import commands

yt_dlp.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = yt_dlp.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        
        if 'entries' in data:
            data = data['entries'][0]
            
        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"), data=data)

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='join', help="Tells the bot to join the voice channel")
    async def join(self, ctx):
        if not ctx.message.author.voice:
            await ctx.send(f"{ctx.message.author.name} is not connected to a voice channel!!!")
            return
        else:
            channel = ctx.message.author.voice.channel
        await channel.connect()

    @commands.command(name='leave', help="To make the bot leave the voice channel")
    async def leave(self, ctx):
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_connected():
            await voice_client.disconnect()
        else:
            await ctx.send("i'm not connected to a voice channel...")
    
    @commands.command(name='play', help="Stream a song from a URL")
    async def play(self, ctx, url):
        server = ctx.message.guild
        voice_channel = server.voice_client
        
        if not voice_channel or not voice_channel.is_connected():
            await ctx.send("i'm not connected to a voice channel...")
            return

        try:
            async with ctx.typing():
                player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
                source = discord.FFmpegPCMAudio(player.url, before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5")
                voice_channel.play(source, after=lambda e: print(f'player error: {e}') if e else None)

            await ctx.send(f'**now playing**: {player.title}')
        except Exception as e:
            print(f"Error: {e}")
            await ctx.send(f"an error occurred: {e}")

    @commands.command(name='pause', help="Pauses the currently playing song")
    async def pause(self, ctx):
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_playing():
            await voice_client.pause()
        else:
            await ctx.send("i'm not playing anything at the moment...")
        
    @commands.command(name='resume', help="Resumes the song")
    async def resume(self, ctx):
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_paused():
            await voice_client.resume()
        else:
            await ctx.send("i wasn't playing anthing...")

    @commands.command(name='stop', help="Stops the song")
    async def stop(self, ctx):
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_playing():
            await voice_client.stop()
        else:
            await ctx.send("i'm not playing anything at the moment...")
