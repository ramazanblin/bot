
import os
import telebot
from flask import Flask, request

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = f"https://{os.getenv('RENDER_EXTERNAL_HOSTNAME')}/"

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

# Bot commands and logic
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Добро пожаловать! Напишите цену кроссовок, и я рассчитаю стоимость с доставкой.")

@bot.message_handler(func=lambda message: message.text.startswith("Курс:"))
def set_exchange_rate(message):
    try:
        rate = float(message.text.split(":")[1].strip())
        with open("exchange_rate.txt", "w") as f:
            f.write(str(rate))
        bot.reply_to(message, f"Курс юаня установлен: {rate} руб.")
    except Exception:
        bot.reply_to(message, "Ошибка: введите курс в формате 'Курс: число'.")

@bot.message_handler(func=lambda message: True)
def calculate_price(message):
    try:
        with open("exchange_rate.txt", "r") as f:
            rate = float(f.read().strip())
        price = float(message.text.strip())
        total = price * rate
        bot.reply_to(message, f"Цена с учетом доставки: {total:.2f} руб.")
    except FileNotFoundError:
        bot.reply_to(message, "Курс юаня еще не установлен. Обратитесь к администратору.")
    except ValueError:
        bot.reply_to(message, "Введите корректную цену или команду.")

# Flask routes
@app.route("/", methods=["GET", "POST"])
def webhook():
    if request.method == "POST":
        json_str = request.get_data().decode("UTF-8")
        update = telebot.types.Update.de_json(json_str)
        bot.process_new_updates([update])
        return "OK", 200
    return "Бот работает!", 200

if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL)
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
