import os
import asyncio
from flask import Flask, request, jsonify
from telegram import Update
from bot import application

app = Flask(__name__)

async def process_update(update):
    await application.process_update(update)

@app.route(f'/{os.getenv("BOT_TOKEN")}', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(), application.bot)
    asyncio.run(process_update(update))
    return jsonify({"status": "success"})

@app.route('/')
def home():
    return "Ethiopian Uni Dating Bot is running! Use /start in Telegram"

@app.route('/test-db')
async def test_db():
    try:
        conn = await asyncpg.connect(os.getenv('DATABASE_URL'))
        await conn.close()
        return "Database connection successful!", 200
    except Exception as e:
        return f"Database error: {str(e)}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 10000)))
