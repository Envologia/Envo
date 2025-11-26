# Envo Userbot - AFK Plugin (Redis-backed)
# Created by @envologia

import time
from telethon import events
from pyEnvo.redis import redis_client

r = redis_client()

def is_afk():
    return r.get("envo_afk") == "true" if r else False

def set_afk(reason):
    if r:
        r.set("envo_afk", "true")
        r.set("envo_afk_reason", reason)
        r.set("envo_afk_start_time", str(time.time()))

def unset_afk():
    if r:
        r.delete("envo_afk", "envo_afk_reason", "envo_afk_start_time")

def get_afk_reason():
    return r.get("envo_afk_reason") if r else "No reason provided."

def get_afk_start_time():
    start_time = r.get("envo_afk_start_time") if r else None
    return float(start_time) if start_time else None

def register(envo):
    @envo.on(events.NewMessage(pattern=r"\.afk(?:\s+(.*)|$)", outgoing=True))
    async def go_afk(event):
        """Command to go AFK."""
        if not r:
            await event.edit("Redis is not connected. AFK feature is disabled.")
            return

        reason = event.pattern_match.group(1) or "No reason provided."
        set_afk(reason)
        await event.edit(f"I am now AFK. Reason: {reason}")

    @envo.on(events.NewMessage(outgoing=True, func=lambda e: not e.text.startswith('.afk')))
    async def stop_afk(event):
        """Stop AFK when any message is sent."""
        if is_afk():
            start_time = get_afk_start_time()
            unset_afk()
            if start_time:
                end_time = time.time()
                duration = time.strftime("%Hh %Mm %Ss", time.gmtime(end_time - start_time))
                await event.respond(f"I'm back! I was AFK for {duration}.")

    @envo.on(events.NewMessage(incoming=True))
    async def afk_reply(event):
        """Reply to messages when AFK."""
        if not is_afk():
            return

        # Don't reply to bots or in channels
        sender = await event.get_sender()
        if not sender or sender.bot or event.is_channel:
            return

        # Check for mentions or replies
        mentioned = await event.is_mentioned()
        replied_to_me = False
        if event.message.reply_to_msg_id:
            reply_msg = await event.get_reply_message()
            if reply_msg and reply_msg.sender_id == (await event.client.get_me()).id:
                replied_to_me = True

        if mentioned or replied_to_me or event.is_private:
            start_time = get_afk_start_time()
            duration = ""
            if start_time:
                duration = time.strftime("%Hh %Mm %Ss", time.gmtime(time.time() - start_time))

            await event.reply(
                f"I am currently AFK.\n"
                f"Reason: {get_afk_reason()}\n"
                f"Away for: {duration}"
            )
