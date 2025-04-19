from flask import Flask, request, jsonify
import os
from telegram import Update
from bot import application  # Import from your bot.py

app = Flask(__name__)

@app.route('/')
def health_check():
    return jsonify({"status": "healthy", "service": "Ethiopian Dating Bot"})

@app.route(f'/{os.getenv("BOT_TOKEN")}', methods=['POST'])
def webhook():
    if request.method == 'POST':
        update = Update.de_json(request.get_json(force=True), application.bot)
        application.process_update(update)
        return jsonify({"status": "success"})
    return jsonify({"status": "error"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 10000)))
