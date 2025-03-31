import discord
import textwrap
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from io import BytesIO
from discord.ext import commands

class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='seagal', help="big ball seagal")
    async def seagal(self, ctx, text: str):        
        font = ImageFont.truetype('resources/impact.ttf', 128)

        img = Image.open('resources/seagal.jpg')
        
        W, H = img.size
        
        draw = ImageDraw.Draw(img)

        lines = textwrap.wrap(text, width=26)
        text = "\n".join(lines)
        
        _, _, _, h = draw.multiline_textbbox((0, 0), 
                                            text=text.upper(), 
                                            font=font,
                                            align='center')
        y_pos = H - h

        draw.multiline_text((W/2, y_pos),
                            text=text.upper(), 
                            font=font, 
                            fill='white',
                            stroke_width=10,
                            stroke_fill='black',
                            anchor='ms',
                            align='center')
        
        with BytesIO() as img_binary:
            img.save(img_binary, 'PNG')
            img_binary.seek(0)
            await ctx.send(file=discord.File(fp=img_binary, filename='image.png'))
    