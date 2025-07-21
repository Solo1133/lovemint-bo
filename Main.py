import telebot
from gtts import gTTS
import os
import requests

# --- CONFIGURATION ---
API_TOKEN = '7991119314:AAFrZhBA2piVSzQfEsZutPx3FMU5FInC2uY'  # Replace with your real token
FREE_AI_CHAT_API = 'https://api.affiliateplus.xyz/api/chat?botname=LoveMint&ownername=Admin&userid={}&msg={}'

# Coins & User Data
user_data = {}

bot = telebot.TeleBot(API_TOKEN)

# --- UTILITIES ---
def get_ai_reply(user_id, msg):
    url = FREE_AI_CHAT_API.format(user_id, requests.utils.quote(msg))
    response = requests.get(url).json()
    return response.get('message', "Sorry, I couldn't understand.")

def text_to_voice(text, lang='en'):
    tts = gTTS(text=text, lang=lang)
    filename = f"voice_{os.getpid()}.ogg"
    tts.save(filename)
    return filename

# --- COMMANDS ---
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    if user_id not in user_data:
        user_data[user_id] = {'coins': 10, 'vip': False}
    bot.reply_to(message, "👋 Welcome to LoveMint AI!\n💬 Chat with me using text.\n🎧 Send /voice before your message for voice replies!\n💰 You have {} coins.".format(user_data[user_id]['coins']))

@bot.message_handler(commands=['balance'])
def show_balance(message):
    user_id = message.from_user.id
    coins = user_data.get(user_id, {}).get('coins', 0)
    bot.reply_to(message, f"💰 You have {coins} coins.")

@bot.message_handler(commands=['vip'])
def show_vip(message):
    user_id = message.from_user.id
    vip = user_data.get(user_id, {}).get('vip', False)
    bot.reply_to(message, "🌟 You are a VIP user!" if vip else "🚫 You are not a VIP. Contact admin to upgrade.")

# --- VOICE CHAT ---
@bot.message_handler(func=lambda m: m.text.startswith('/voice'))
def voice_reply(message):
    user_id = message.from_user.id
    if user_data[user_id]['coins'] <= 0:
        bot.reply_to(message, "❌ Not enough coins. Use /balance to check.")
        return
    msg = message.text.replace('/voice', '').strip()
    reply = get_ai_reply(user_id, msg)
    voice_file = text_to_voice(reply)
    with open(voice_file, 'rb') as v:
        bot.send_voice(message.chat.id, v)
    os.remove(voice_file)
    user_data[user_id]['coins'] -= 1

# --- TEXT CHAT ---
@bot.message_handler(func=lambda m: True)
def handle_text(message):
    user_id = message.from_user.id
    if user_data[user_id]['coins'] <= 0:
        bot.reply_to(message, "❌ Not enough coins. Use /balance to check.")
        return
    reply = get_ai_reply(user_id, message.text)
    bot.reply_to(message, reply)
    user_data[user_id]['coins'] -= 1

# --- START BOT ---
bot.polling()
