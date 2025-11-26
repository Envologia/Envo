# Envo Userbot - Animation Plugins
# Created by @envologia

import asyncio
from telethon import events

async def animate_text(event, text_animation):
    """Helper function to animate text."""
    for frame in text_animation:
        await event.edit(frame)
        await asyncio.sleep(0.3)

def register(envo):
    @envo.on(events.NewMessage(pattern=r"\.lmao", outgoing=True))
    async def lmao(event):
        animation = [
            "😂",
            "🤣",
            "😆",
            "😹",
            "😂",
            "🤣",
            "😆",
            "😹",
        ]
        await animate_text(event, animation)

    @envo.on(events.NewMessage(pattern=r"\.heart", outgoing=True))
    async def heart(event):
        animation = [
            "❤️",
            "🧡",
            "💛",
            "💚",
            "💙",
            "💜",
            "🖤",
            "🤍",
        ]
        await animate_text(event, animation)

    @envo.on(events.NewMessage(pattern=r"\.bomb", outgoing=True))
    async def bomb(event):
        animation = [
            "💣",
            "💥",
            "🔥",
            "💨",
            "✨",
        ]
        await animate_text(event, animation)
