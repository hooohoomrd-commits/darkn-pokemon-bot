from telegram.ext import Updater, CommandHandler
import random, os

TOKEN = os.getenv("BOT_TOKEN")

updater = Updater(TOKEN, use_context=True)
dp = updater.dispatcher

# ---------------- DATA ----------------
normal_pokemon = ["Pikachu", "Charmander", "Bulbasaur", "Squirtle"]
legendary_pokemon = ["Mewtwo", "Rayquaza", "Lugia"]
mega_pokemon = ["Mega Charizard", "Mega Blastoise"]

users = {}
wild_pokemon = {}

# ---------------- HELPERS ----------------
def get_user(uid):
    if uid not in users:
        users[uid] = {
            "coins": 500,
            "bag": {"pokeball": 5},
            "pokemon": []
        }
    return users[uid]

# ---------------- COMMANDS ----------------
def start(update, context):
    update.message.reply_text(
        "🔥 DARKN Pokémon Bot\n\n"
        "/summon\n/catch\n/bag\n/mypokemon\n"
        "/balance\n/buyball\n/challenge @user"
    )

def summon(update, context):
    uid = update.effective_user.id

    roll = random.randint(1, 100)

    if roll <= 2:
        name = random.choice(mega_pokemon)
        rarity = "💎 MEGA"
    elif roll <= 7:
        name = random.choice(legendary_pokemon)
        rarity = "🌟 LEGENDARY"
    else:
        name = random.choice(normal_pokemon)
        rarity = "⚪ NORMAL"

    level = random.randint(1, 20)

    wild_pokemon[uid] = {"name": name, "level": level, "rarity": rarity}

    update.message.reply_text(
        f"{rarity} Pokémon appeared!\n"
        f"{name} (Lv {level})\n"
        f"Use /catch"
    )

def catch(update, context):
    uid = update.effective_user.id
    user = get_user(uid)

    if uid not in wild_pokemon:
        update.message.reply_text("❌ No Pokémon to catch.")
        return

    if user["bag"]["pokeball"] <= 0:
        update.message.reply_text("❌ No Pokéballs.")
        return

    poke = wild_pokemon[uid]
    user["bag"]["pokeball"] -= 1

    chance = 70 - poke["level"] * 2
    if poke["rarity"] == "🌟 LEGENDARY":
        chance -= 20
    if poke["rarity"] == "💎 MEGA":
        chance -= 30

    if random.randint(1, 100) <= chance:
        user["pokemon"].append(poke)
        reward = poke["level"] * 20
        user["coins"] += reward

        update.message.reply_text(
            f"🎉 Caught {poke['name']}!\n"
            f"+{reward} coins"
        )
        del wild_pokemon[uid]
    else:
        update.message.reply_text("💨 It escaped!")

def bag(update, context):
    user = get_user(update.effective_user.id)
    update.message.reply_text(
        f"🎒 Pokéballs: {user['bag']['pokeball']}\n"
        f"💰 Coins: {user['coins']}"
    )

def buyball(update, context):
    user = get_user(update.effective_user.id)

    if user["coins"] < 50:
        update.message.reply_text("❌ Not enough coins.")
        return

    user["coins"] -= 50
    user["bag"]["pokeball"] += 1
    update.message.reply_text("✅ Bought 1 Pokéball (50 coins)")

def mypokemon(update, context):
    user = get_user(update.effective_user.id)

    if not user["pokemon"]:
        update.message.reply_text("❌ No Pokémon.")
        return

    msg = "📕 Your Pokémon:\n"
    for i, p in enumerate(user["pokemon"], 1):
        msg += f"{i}. {p['name']} (Lv {p['level']}) {p['rarity']}\n"

    update.message.reply_text(msg)

def balance(update, context):
    user = get_user(update.effective_user.id)
    update.message.reply_text(f"💰 Coins: {user['coins']}")

def challenge(update, context):
    uid = update.effective_user.id
    user = get_user(uid)

    if not context.args:
        update.message.reply_text("❌ Use /challenge @user")
        return

    if not user["pokemon"]:
        update.message.reply_text("❌ You have no Pokémon.")
        return

    opponent_name = context.args[0]

    my_poke = random.choice(user["pokemon"])
    my_power = my_poke["level"] + random.randint(1, 10)

    update.message.reply_text(
        f"⚔️ Challenge sent to {opponent_name}\n"
        f"Your Pokémon: {my_poke['name']} (Lv {my_poke['level']})\n"
        f"Power: {my_power}\n\n"
        f"(PvP auto-resolve demo)"
    )

# ---------------- HANDLERS ----------------
dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler("summon", summon))
dp.add_handler(CommandHandler("catch", catch))
dp.add_handler(CommandHandler("bag", bag))
dp.add_handler(CommandHandler("buyball", buyball))
dp.add_handler(CommandHandler("mypokemon", mypokemon))
dp.add_handler(CommandHandler("balance", balance))
dp.add_handler(CommandHandler("challenge", challenge))

updater.start_polling()
updater.idle()
