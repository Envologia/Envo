# Envo Userbot Assistant
# Created by @envologia

import os
from telethon import TelegramClient, events
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

assistant = TelegramClient("assistant", os.getenv("API_KEY"), os.getenv("API_HASH")).start(bot_token=BOT_TOKEN)

@assistant.on(events.NewMessage(pattern="/start"))
async def start(event):
    await event.reply("Envo Userbot assistant is alive!")

def main():
    assistant.run_until_disconnected()

if __name__ == "__main__":
    main()
