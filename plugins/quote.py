# Envo Userbot - Quote Plugin
# Created by @envologia

import httpx
from telethon import events

async def get_random_quote():
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get("https://api.quotable.io/random")
            response.raise_for_status()
            data = response.json()
            return f"\"{data['content']}\" - {data['author']}"
        except Exception as e:
            return f"An error occurred: {e}"

def register(envo):
    @envo.on(events.NewMessage(pattern=r"\.quote", outgoing=True))
    async def quote(event):
        random_quote = await get_random_quote()
        await event.edit(random_quote)
