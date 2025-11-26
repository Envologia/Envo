# Envo Userbot - Memify Plugin
# Created by @envologia

from telethon import events
from PIL import Image, ImageDraw, ImageFont
import io

def draw_text_on_image(image_bytes, text):
    """Draws text on an image."""
    image = Image.open(io.BytesIO(image_bytes))
    draw = ImageDraw.Draw(image)

    # Use a font
    try:
        font = ImageFont.truetype("resources/DejaVuSans.ttf", 30)
    except IOError:
        font = ImageFont.load_default()

    # Add text to the top of the image
    draw.text((10, 10), text, fill='white', font=font, stroke_width=2, stroke_fill='black')

    output_image = io.BytesIO()
    image.save(output_image, "PNG")
    output_image.seek(0)
    return output_image

def register(envo):
    @envo.on(events.NewMessage(pattern=r"\.meme(?:\s+(.*)|$)", outgoing=True))
    async def memify(event):
        text = event.pattern_match.group(1)
        reply_message = await event.get_reply_message()

        if not text or not reply_message or not reply_message.photo:
            await event.edit("Please reply to a photo with text to create a meme.")
            return

        image_bytes = await reply_message.download_media(bytes)
        meme_image = draw_text_on_image(image_bytes, text)

        await event.delete()
        await event.respond(file=meme_image)
