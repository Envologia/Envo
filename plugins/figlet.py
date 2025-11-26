# Envo Userbot - Figlet Plugin
# Created by @envologia

import pyfiglet
from telethon import events

def register(envo):
    @envo.on(events.NewMessage(pattern=r"\.figlet\s+(.*)", outgoing=True))
    async def figlet(event):
        text = event.pattern_match.group(1)
        ascii_art = pyfiglet.figlet_format(text)
        await event.edit(f"```{ascii_art}```")
