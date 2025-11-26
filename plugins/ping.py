# Envo Userbot
# Created by @envologia

from telethon import events

def register(envo):
    @envo.on(events.NewMessage(pattern=r"\.ping", outgoing=True))
    async def ping(event):
        await event.edit("Pong!")
