from flask import Flask, request
import telebot
import os

TOKEN = os.getenv("TOKEN")
RENDER_URL = os.getenv("RENDER_EXTERNAL_URL")  # Render автоматически передаст URL
bot = telebot.TeleBot(TOKEN)

app = Flask(__name__)

@app.route('/' + TOKEN, methods=['POST'])
def webhook():
    json_data = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_data)
    bot.process_new_updates([update])
    return '!', 200

@app.route('/')
def index():
    return "Bot is running!"

if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url="https://api.render.com/deploy/srv-ctt5sd5ds78s73ckj01g?key=-U_No4RlTPw/" + TOKEN)
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
