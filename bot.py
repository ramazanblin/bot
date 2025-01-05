
import os
import telebot

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Напиши цену кроссовок, и я рассчитаю стоимость с учётом доставки.")

bot.polling(non_stop=True)
