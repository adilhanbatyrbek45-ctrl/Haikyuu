import telebot
from telebot import types
import json
import random
import os
from datetime import datetime



class Card:
    def __init__(self, name, team, rating, price, photo_path):
        self.name = name
        self.team = team
        self.rating = rating
        self.price = price
        self.sell_price = price // 2
        self.photo_path = photo_path
        self.position = "General" 


    def get_info(self):
        return "🏐 Player: {}\n🏠 Team: {}\n⭐ Rating: {}\n💰 Value: {} coins".format(
            self.name, self.team, self.rating, self.price
        )


class Setter(Card):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.position = "Setter"

    def get_info(self):
        basic = super().get_info()
        return "🧩 Position: {}\n{} \n🎯 Skill: Master of Toss".format(self.position, basic)


class Spiker(Card):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.position = "Spiker"

    def get_info(self):
        basic = super().get_info()
        return "🔨 Position: {}\n{}\n🔥 Skill: Powerful Spike".format(self.position, basic)


class Libero(Card):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.position = "Libero"

    def get_info(self):
        basic = super().get_info()
        return "🛡️ Position: {}\n{} \n🧤 Skill: Perfect Reception".format(self.position, basic)


DATA_FILE = 'players_data.json'

def load_data():
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    except Exception as e:
        print("Loading error: {}".format(e))
        return {}

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


TOKEN = '8993322812:AAFSYrZIheGiP3K33uk19V3ySkXMlkV6X8g'
bot = telebot.TeleBot(TOKEN)


POOL = [
    Spiker("Shoyo Hinata", "Karasuno", 85, 500, "images/hinata.jpg"),
    Setter("Tobio Kageyama", "Karasuno", 87, 600, "images/kageyama.jpg"),
    Setter("Kenma Kozume", "Nekoma", 87, 600, "images/kenma.jpg"),
    Setter("Toru Oikawa", "Aoba Johsai", 91, 800, "images/oikawa.jpg"),
    Spiker("Kei Tsukishima", "Karasuno", 88, 700, "images/tsukishima.jpg"),
    Setter("Keiji Akaashi", "Fukurodani", 88, 700, "images/Akaashi.jpg"),
    Spiker("Azumane Asahi", "Karasuno", 86, 500, "images/asahi.jpg"),
    Spiker("Udai Tenma", "Karasuno", 99, 10000, "images/tenma.jpg"),
    Setter("Atsumu Miya", "Inaridzaki", 92, 1000, "images/atsumu.jpg"),
    Spiker("Kotaro Bokuto", "Fukurodani", 90, 800, "images/bokuto.jpg"),
    Spiker("Hajime Iwaizumi", "Aoba Johsai", 81, 300, "images/iwaizumi.jpg"),
    Libero("Tetsuro Kuroo", "Nekoma", 90, 800, "images/kuroo.jpg"),
    Libero("Yu Nishinoya", "Karasuno", 85, 800, "images/nishinoya.jpg"),
    Setter("Koshi Sugawara", "Nekoma", 90, 800, "images/kuroo.jpg"),
    Card("Alibek", "Mama", 101, 10000, "images/alibek.jpg"), 
    Card("Dauletqali", "Osel", 101, 10000, "images/Dauletqali.jpg")
]


def init_user(user_id, username, data):
    if user_id not in data:
        data[user_id] = {
            "username": username,
            "balance": 1000,
            "inventory": [],
            "rolls_today": 0,
            "last_roll_date": ""
        }
    else:
        data[user_id]["username"] = username
    return data

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = str(message.from_user.id)
    username = message.from_user.first_name or "Player"
    data = load_data()
    data = init_user(user_id, username, data)
    save_data(data)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        types.KeyboardButton("🎲 Daily Roll"),
        types.KeyboardButton("🎒 Inventory"),
        types.KeyboardButton("🛍️ Shop"),
        types.KeyboardButton("💰 Balance & Top-Up"),
        types.KeyboardButton("🏆 Leaderboard"),
        types.KeyboardButton("🎰 Casino"),
    )
    bot.send_message(message.chat.id, "Welcome to Haikyuu Card Game! Choose an option:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "💰 Balance & Top-Up")
def check_balance(message):
    user_id = str(message.from_user.id)
    data = load_data()
    balance = data.get(user_id, {}).get("balance", 0)
    markup = types.InlineKeyboardMarkup()
    donate_btn = types.InlineKeyboardButton("🎁 Claim Daily Bonus (+500)", callback_data="topup")
    markup.add(donate_btn)
    bot.send_message(message.chat.id, "Your balance: {} coins".format(balance), reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "🎲 Daily Roll")
def daily_roll(message):
    user_id = str(message.from_user.id)
    data = load_data()
    data = init_user(user_id, message.from_user.first_name, data)
    today = datetime.now().strftime("%Y-%m-%d")
    if data[user_id].get("last_roll_date") != today:
        data[user_id]["rolls_today"] = 0
        data[user_id]["last_roll_date"] = today
    rolls_done = data[user_id]["rolls_today"]
    if rolls_done >= 5:
        bot.send_message(message.chat.id, "❌ You have reached your daily limit (5/5). Come back tomorrow!")
        return
    card = random.choice(POOL)
    data[user_id]["inventory"].append(card.name)
    data[user_id]["rolls_today"] += 1
    save_data(data)
    rolls_left = 5 - data[user_id]["rolls_today"]
    try:
        with open(card.photo_path, 'rb') as photo:
            bot.send_photo(message.chat.id, photo, caption="🎉 You rolled:\n\n{}\n\nRolls left today: {}".format(card.get_info(), rolls_left))
    except FileNotFoundError:
        bot.send_message(message.chat.id, "You rolled:\n\n{}\n\nRolls left today: {}\n(Photo missing)".format(card.get_info(), rolls_left))

@bot.message_handler(func=lambda message: message.text == "🛍️ Shop")
def open_shop(message):
    card = random.choice(POOL)
    markup = types.InlineKeyboardMarkup()
    buy_btn = types.InlineKeyboardButton("Buy for {} coins".format(card.price), callback_data="buy_{}".format(card.name))
    markup.add(buy_btn)
    try:
        with open(card.photo_path, 'rb') as photo:
            bot.send_photo(message.chat.id, photo, caption="On sale:\n\n{}".format(card.get_info()), reply_markup=markup)
    except FileNotFoundError:
        bot.send_message(message.chat.id, "On sale:\n\n{}\n\n(Photo missing)".format(card.get_info()), reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "🎒 Inventory")
def show_inventory(message):
    user_id = str(message.from_user.id)
    data = load_data()
    inv = data.get(user_id, {}).get("inventory", [])
    if not inv:
        bot.send_message(message.chat.id, "Your inventory is empty.")
        return
    markup = types.InlineKeyboardMarkup(row_width=1)
    inventory_counts = {}
    for item in inv:
        inventory_counts[item] = inventory_counts.get(item, 0) + 1
    text_lines = ["Your players: "]
    for item, count in inventory_counts.items():
        card = next((c for c in POOL if c.name == item), None)
        if card:
            text_lines.append("- {} x{} (⭐ {})".format(item, count, card.rating))
            sell_btn = types.InlineKeyboardButton("Sell 1 {} (+{})".format(item, card.sell_price), callback_data="sell_{}".format(item))
            markup.add(sell_btn)
    bot.send_message(message.chat.id, "\n".join(text_lines), reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "🏆 Leaderboard")
def show_leaderboard(message):
    try:
        data = load_data()
        if not data:
            bot.send_message(message.chat.id, "🏆 Leaderboard is currently empty. Be the first!")
            return
        leaderboard = []
        for uid, udata in data.items():
            if not isinstance(udata, dict):
                continue
            total_rating = 0
            inv = udata.get("inventory", [])
            for item in inv:
                card = next((c for c in POOL if c.name == item), None)
                if card:
                    total_rating += card.rating
            username = udata.get("username") or "Player {}".format(uid[-4:])
            leaderboard.append((username, total_rating))
        if not leaderboard:
            bot.send_message(message.chat.id, "🏆 No active players in leaderboard yet.")
            return
        leaderboard.sort(key=lambda x: x[1], reverse=True)
        lines = ["🏆 GLOBAL LEADERBOARD (By Total Rating) 🏆\n"]
        for i, (uname, rating) in enumerate(leaderboard[:10]):
            lines.append("{}. {} - ⭐ {}".format(i+1, uname, rating))
        bot.send_message(message.chat.id, "\n".join(lines))
    except Exception as e:
        print("Leaderboard error: {}".format(e))
        bot.send_message(message.chat.id, "⚠️ Sorry, an error occurred while loading the leaderboard.")

@bot.callback_query_handler(func=lambda call: call.data == 'topup')
def handle_topup(call):
    user_id = str(call.from_user.id)
    data = load_data()
    today = datetime.now().strftime("%Y-%m-%d")
    last_bonus = data[user_id].get("last_bonus_date", "")
    if last_bonus == today:
        bot.answer_callback_query(call.id, "⏳ You already claimed your bonus today!\nCome back tomorrow.", show_alert=True)
    else:
        data[user_id]["balance"] += 500
        data[user_id]["last_bonus_date"] = today
        save_data(data)
        bot.answer_callback_query(call.id, "🎉 +500 coins! Daily bonus claimed.")
        bot.edit_message_text("Your balance: {} coins\n\n✅ Daily bonus claimed today.".format(data[user_id]["balance"]), chat_id=call.message.chat.id, message_id=call.message.message_id)

@bot.callback_query_handler(func=lambda call: call.data.startswith('buy_'))
def handle_buy(call):
    user_id = str(call.from_user.id)
    card_name = call.data.split('_')[1]
    data = load_data()
    card = next((c for c in POOL if c.name == card_name), None)
    if card and data[user_id]["balance"] >= card.price:
        data[user_id]["balance"] -= card.price
        data[user_id]["inventory"].append(card.name)
        save_data(data)
        bot.answer_callback_query(call.id, "Successfully bought!")
        bot.edit_message_caption("✅ Purchased: {}".format(card.name), chat_id=call.message.chat.id, message_id=call.message.message_id)
    else:
        bot.answer_callback_query(call.id, "Not enough coins!")

@bot.callback_query_handler(func=lambda call: call.data.startswith('sell_'))
def handle_sell(call):
    user_id = str(call.from_user.id)
    card_name = call.data.split('_')[1]
    data = load_data()
    inv = data.get(user_id, {}).get("inventory", [])
    if card_name in inv:
        card = next((c for c in POOL if c.name == card_name), None)
        if card:
            inv.remove(card_name)
            data[user_id]["balance"] += card.sell_price
            save_data(data)
            bot.answer_callback_query(call.id, "Sold for {} coins!".format(card.sell_price))
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            bot.send_message(call.message.chat.id, "✅ {} was sold. Check /start for menu.".format(card.name))
    else:
        bot.answer_callback_query(call.id, "You don't have this card!")

@bot.message_handler(func=lambda message: message.text == "🎰 Casino")
def casino_start(message):
    user_id = str(message.from_user.id)
    data = load_data()
    if user_id not in data:
        bot.send_message(message.chat.id, "Please type /start first to register!")
        return
    balance = data.get(user_id, {}).get("balance", 0)
    if balance <= 0:
        bot.send_message(message.chat.id, "❌ You are broke! You need coins to play.")
        return
    msg = bot.send_message(message.chat.id, "Welcome to the Casino! 🎰\nYour balance: {} coins.\n\nEnter your bet amount (type a number):".format(balance))
    bot.register_next_step_handler(msg, process_bet)

def process_bet(message):
    user_id = str(message.from_user.id)
    data = load_data()
    if message.text in ["🎲 Daily Roll", "🎒 Inventory", "🛍️ Shop", "💰 Balance & Top-Up", "🏆 Leaderboard", "🎰 Casino"]:
        bot.send_message(message.chat.id, "Bet cancelled. Returning to menu.")
        return
    if not message.text.isdigit():
        bot.send_message(message.chat.id, "⚠️ Invalid input. Please enter numbers only! Try clicking 🎰 Casino again.")
        return
    bet = int(message.text)
    balance = data.get(user_id, {}).get("balance", 0)
    if bet <= 0:
        bot.send_message(message.chat.id, "⚠️ Bet must be greater than 0!")
        return
    if bet > balance:
        bot.send_message(message.chat.id, "❌ Not enough coins! Your balance is only {}.".format(balance))
        return
    data[user_id]["balance"] -= bet
    if random.choice([True, False]):
        win_amount = bet * 2
        data[user_id]["balance"] += win_amount
        save_data(data)
        bot.send_message(message.chat.id, "🎲 The coin flipped... HEADS!\n\n🎉 YOU WON {} coins! 🎉\nNew balance: {}".format(win_amount, data[user_id]["balance"]))
    else:
        save_data(data)
        bot.send_message(message.chat.id, "🎲 The coin flipped... TAILS!\n\n💸 You lost {} coins.\nNew balance: {}".format(bet, data[user_id]["balance"]))

if __name__ == "__main__":
    print("Bot is running...")
    bot.infinity_polling()