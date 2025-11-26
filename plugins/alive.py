# Envo Userbot
# Created by @envologia

from telethon import events

def register(envo):
    @envo.on(events.NewMessage(pattern=r"\.alive", outgoing=True))
    async def alive(event):
        await event.edit("Envo Userbot is alive!")
