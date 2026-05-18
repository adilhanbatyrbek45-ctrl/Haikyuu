# Haikyuu
🏐 Haikyuu Card Game Bot (Telegram)

A Telegram bot featuring a card collection system inspired by Haikyuu characters, an economy system, casino gameplay, and inventory management.

📌 Description

This bot allows users to:

🎲 Roll random player cards
🛍️ Buy cards from the shop
🎒 Manage their inventory
💰 Earn and spend coins
🎰 Play casino games
🏆 Compete on the global leaderboard

All user data is stored locally in a JSON file.

⚙️ Installation

Clone the repository:
git clone https://github.com/your-repo/haikyuu-bot.git
cd haikyuu-bot

Install dependencies:
pip install pyTelegramBotAPI

🚀 Run the Bot

Start the bot with:
python main.py

🔑 Configuration

Set your Telegram bot token inside the code:
TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'

Important: Never expose your real bot token publicly.

🧠 Main Features

🎲 Daily Roll — Get a random player card (up to 5 rolls per day)

🛍️ Shop — Buy a random card using coins

🎒 Inventory — View and sell collected cards

💰 Balance & Daily Bonus — Check balance and claim +500 daily coins

🎰 Casino — Bet coins with a 50/50 chance to double or lose your bet

🏆 Leaderboard — Global ranking based on total card ratings

📦 Data Structure

Stored in: players_data.json

Example:
{
"123456789": {
"username": "Player",
"balance": 1000,
"inventory": ["Hinata Shoyo"],
"rolls_today": 2,
"last_roll_date": "2026-05-18",
"last_bonus_date": "2026-05-18"
}
}

🧩 Cards

Each card includes:

Player name
Team
Rating
Price
Position (Setter / Spiker / Libero)
📚 Technologies Used
Python 3
pyTelegramBotAPI (telebot)
JSON for data storage
random, datetime, os modules
⚠️ Important Notes
All data is stored locally (no database)
Deleting the JSON file resets all progress
The bot is not protected against multi-account abuse or cheating
💡 Possible Improvements
Add SQLite or PostgreSQL database
Introduce card rarity system (common, rare, legendary)
PvP battles system
Player trading system
Card packs and events

This project was created for educational purposes.
