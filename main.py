
import os
import logging
from flask import Flask
from telebot import TeleBot, types

# Telegram Bot Token
BOT_TOKEN = "8170255604:AAFfGhtl1vsYJE4lQQKRvtekCeg1lqrKGiY"
bot = TeleBot(BOT_TOKEN)

# Flask app для Render
app = Flask(__name__)

# Логирование
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Хранение курса юаня
yuan_rate = None
admin_id = 322878067  # Ваш Telegram ID

@bot.message_handler(commands=['start'])
def send_welcome(message):
    global yuan_rate
    if message.from_user.id == admin_id:
        if yuan_rate is None:
            bot.reply_to(message, "Привет! Установите курс юаня на сегодня в формате: Курс: число")
        else:
            bot.reply_to(message, "Привет! Вы можете изменить курс юаня или посчитать стоимость кроссовок.")
    else:
        bot.reply_to(message, "Привет! Напишите цену кроссовок, и я посчитаю стоимость с учётом доставки.")

@bot.message_handler(func=lambda message: message.from_user.id == admin_id and message.text.startswith("Курс:"))
def set_yuan_rate(message):
    global yuan_rate
    try:
        yuan_rate = float(message.text.split(":")[1].strip())
        bot.reply_to(message, f"Курс юаня установлен: {yuan_rate} руб.")
        logger.info(f"Курс юаня установлен: {yuan_rate} руб.")
    except ValueError:
        bot.reply_to(message, "Некорректный формат. Введите курс в формате: Курс: число.")

@bot.message_handler(func=lambda message: True)
def calculate_price(message):
    global yuan_rate
    if yuan_rate is None:
        bot.reply_to(message, "Курс юаня ещё не установлен. Обратитесь к администратору.")
        return

    try:
        price_in_yuan = float(message.text.strip())
        price_in_rub = price_in_yuan * yuan_rate + 500  # Допустим, 500 руб. доставка
        bot.reply_to(message, f"Цена кроссовок с учётом доставки: {price_in_rub:.2f} руб.")
    except ValueError:
        bot.reply_to(message, "Введите корректную цену в юанях.")

@app.route('/')
def home():
    return "Бот работает!"

def start_web_server():
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

def start_bot():
    bot.polling(none_stop=True)

if __name__ == '__main__':
    import threading
    bot_thread = threading.Thread(target=start_bot)
    bot_thread.start()

    web_thread = threading.Thread(target=start_web_server)
    web_thread.start()
