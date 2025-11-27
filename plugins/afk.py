# Envo Userbot - AFK Plugin (SQLite-backed)
# Created by @envologia

import time
from telethon import events
from pyEnvo.database import get_db_connection

def is_afk():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT is_afk FROM afk WHERE id = 1")
    result = cursor.fetchone()
    conn.close()
    return result["is_afk"] if result else False

def set_afk(reason):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO afk (id, is_afk, reason, start_time) VALUES (1, ?, ?, ?)",
                   (True, reason, time.time()))
    conn.commit()
    conn.close()

def unset_afk():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE afk SET is_afk = ? WHERE id = 1", (False,))
    conn.commit()
    conn.close()

def get_afk_data():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT reason, start_time FROM afk WHERE id = 1")
    result = cursor.fetchone()
    conn.close()
    return result if result else (None, None)

def register(envo):
    @envo.on(events.NewMessage(pattern=r"\.afk(?:\s+(.*)|$)", outgoing=True))
    async def go_afk(event):
        """Command to go AFK."""
        reason = event.pattern_match.group(1) or "No reason provided."
        set_afk(reason)
        await event.edit(f"I am now AFK. Reason: {reason}")

    @envo.on(events.NewMessage(outgoing=True, func=lambda e: not e.text.startswith('.afk')))
    async def stop_afk(event):
        """Stop AFK when any message is sent."""
        if is_afk():
            _, start_time = get_afk_data()
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

        sender = await event.get_sender()
        if not sender or sender.bot or event.is_channel:
            return

        mentioned = await event.is_mentioned()
        replied_to_me = False
        if event.message.reply_to_msg_id:
            reply_msg = await event.get_reply_message()
            if reply_msg and reply_msg.sender_id == (await event.client.get_me()).id:
                replied_to_me = True

        if mentioned or replied_to_me or event.is_private:
            reason, start_time = get_afk_data()
            duration = ""
            if start_time:
                duration = time.strftime("%Hh %Mm %Ss", time.gmtime(time.time() - start_time))

            await event.reply(
                f"I am currently AFK.\n"
                f"Reason: {reason}\n"
                f"Away for: {duration}"
            )
