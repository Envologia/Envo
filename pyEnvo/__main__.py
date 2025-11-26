# Envo Userbot
# Created by @envologia

import os
from telethon import TelegramClient
from dotenv import load_dotenv
from .plugins import load_plugins

load_dotenv()

API_KEY = os.getenv("API_KEY")
API_HASH = os.getenv("API_HASH")
SESSION = os.getenv("SESSION")

envo = TelegramClient(SESSION, API_KEY, API_HASH)

async def main():
    await envo.start()
    load_plugins(envo)
    print("Envo Userbot started!")
    await envo.run_until_disconnected()

if __name__ == "__main__":
    envo.loop.run_until_complete(main())
