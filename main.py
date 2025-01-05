
from flask import Flask, request
import telebot

TOKEN = "YOUR_BOT_TOKEN"
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
    bot.set_webhook(url="YOUR_RENDER_URL/" + TOKEN)
    app.run(host="0.0.0.0", port=10000)
