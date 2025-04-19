from flask import Flask, request
import os
from telegram import Update
from bot import application

app = Flask(__name__)

@app.route('/')
def home():
    return "Ethiopian Uni Dating Bot is running! 🚀"

@app.route(f'/{os.getenv("BOT_TOKEN")}', methods=['POST'])
def telegram_webhook():
    update = Update.de_json(request.get_json(), application.bot)
    application.process_update(update)
    return "OK", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 10000)))
