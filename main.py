import telebot
from gtts import gTTS
import os

API_KEY = "7991119314:AAFrZhBA2piVSzQfEsZutPx3FMU5FInC2uY"

bot = telebot.TeleBot(API_KEY)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Hi, I'm your AI girlfriend! ❤️ How can I make your day better?")

@bot.message_handler(func=lambda m: True)
def echo_all(message):
    response = f"You said: {message.text}"
    bot.reply_to(message, response)

    tts = gTTS(response)
    tts.save("voice.mp3")
    audio = open("voice.mp3", 'rb')
    bot.send_voice(message.chat.id, audio)
    audio.close()
    os.remove("voice.mp3")

bot.infinity_polling()
