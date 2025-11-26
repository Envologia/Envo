# Envo Userbot - .ds Command
# Created by @envologia

from telethon import events
from pyEnvo.ai import get_ai_response

def register(envo):
    @envo.on(events.NewMessage(pattern=r"\.ds(?:\s+(.*)|$)", outgoing=True))
    async def ds(event):
        prompt = event.pattern_match.group(1)
        if not prompt:
            # Check if replying to a message
            reply_message = await event.get_reply_message()
            if reply_message and reply_message.text:
                prompt = reply_message.text
            else:
                await event.edit("Please provide a question or reply to a message.")
                return

        response = await get_ai_response("deepseek/deepseek-chat", prompt)
        await event.edit(response)
