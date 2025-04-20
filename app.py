import os
import asyncio
from flask import Flask, request, jsonify
from telegram import Update
from bot import application  # This connects to your bot.py

app = Flask(__name__)

async def process_update(update):
    try:
        await application.process_update(update)
    except Exception as e:
        app.logger.error(f"Update failed: {e}")

@app.route(f'/{os.getenv("BOT_TOKEN")}', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(), application.bot)
    asyncio.run(process_update(update))
    return jsonify({"status": "ok"})

@app.route('/')
def home():
    return "Bot is running! Send /start in Telegram"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 10000)))
