import os
from dotenv import load_dotenv

load_dotenv()

# MongoDB
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")

# Render
RENDER_URI = os.getenv("RENDER_URI")

# Ticketmaster
API_KEY = os.getenv("API_KEY")
API_URL = f"https://app.ticketmaster.com/discovery/v2/events.json?apikey={API_KEY}"

# Telegram
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
