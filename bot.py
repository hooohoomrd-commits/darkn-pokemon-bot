import telebot
import requests
import random
import os

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "🔥 Welcome to DARKN Pokémon Bot!\nUse /summon to summon a Pokémon.")

@bot.message_handler(commands=['summon'])
def summon(message):
    poke_id = random.randint(1, 898)
    data = requests.get(f"https://pokeapi.co/api/v2/pokemon/{poke_id}").json()
    
    name = data["name"].capitalize()
    image = data["sprites"]["other"]["official-artwork"]["front_default"]
    
    bot.send_photo(
        message.chat.id,
        image,
        caption=f"⚡ A wild Pokémon appeared!\n🔥 **{name}** 🔥",
        parse_mode="Markdown"
    )

bot.infinity_polling()