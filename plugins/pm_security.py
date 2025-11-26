# Envo Userbot - PM Security Plugin (SQLite-backed)
# Created by @envologia

import asyncio
import os
from telethon import events
from pyEnvo.database import get_db_connection
from pyEnvo.captcha import generate_captcha

def is_approved(user_id):
    """Check if a user is approved."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM approved_users WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result is not None

def approve_user(user_id):
    """Approve a user."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO approved_users (user_id) VALUES (?)", (user_id,))
    conn.commit()
    conn.close()

def register(envo):
    @envo.on(events.NewMessage(incoming=True, is_private=True))
    async def pm_security(event):
        sender = await event.get_sender()
        if sender.is_self or sender.bot or is_approved(sender.id):
            return

        captcha_path, correct_answer = generate_captcha()
        try:
            await event.respond(
                "Hello! To prevent spam, please solve this captcha to continue.",
                file=captcha_path
            )

            response = await envo.wait_for(
                events.NewMessage(
                    incoming=True,
                    from_users=sender.id,
                    is_private=True
                ),
                timeout=60
            )

            if response.text == correct_answer:
                approve_user(sender.id)
                await response.respond("Correct! You are now approved.")
            else:
                await response.respond("Incorrect. Please try again later.")
                await envo.block_user(sender.id)

        except asyncio.TimeoutError:
            await event.respond("You did not respond in time. Please try again later.")
            await envo.block_user(sender.id)

        finally:
            if os.path.exists(captcha_path):
                os.remove(captcha_path)
