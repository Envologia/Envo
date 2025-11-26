# Envo Userbot - PM Security Plugin
# Created by @envologia

import asyncio
import os
from telethon import events
from pyEnvo.redis import redis_client
from pyEnvo.captcha import generate_captcha

r = redis_client()

def is_approved(user_id):
    """Check if a user is approved."""
    return r.sismember("envo_approved_users", str(user_id)) if r else False

def approve_user(user_id):
    """Approve a user."""
    if r:
        r.sadd("envo_approved_users", str(user_id))

def register(envo):
    @envo.on(events.NewMessage(incoming=True, is_private=True))
    async def pm_security(event):
        sender = await event.get_sender()
        if sender.is_self or sender.bot or is_approved(sender.id):
            return

        # Generate and send the captcha
        captcha_path, correct_answer = generate_captcha()
        try:
            await event.respond(
                "Hello! To prevent spam, please solve this captcha to continue.",
                file=captcha_path
            )

            # Wait for the user's response
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
            # Clean up the captcha image
            if os.path.exists(captcha_path):
                os.remove(captcha_path)
