import textwrap
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

try:
    text = "when I was a young boy, I found myself lost at the target. This terrible experience was prompted by my mother's sudden disappearance..."
    
    font = ImageFont.truetype('impact.ttf', 140)

    img = Image.open('seagal.jpg')
    
    W, H = img.size
    
    draw = ImageDraw.Draw(img)

    lines = textwrap.wrap(text, width=24)
    text = "\n".join(lines)
    
    left, top, w, h = draw.multiline_textbbox((0, 0), 
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
    
    img.save('image.png')
except Exception as err:
    print(f"**ERROR**: {err}")
