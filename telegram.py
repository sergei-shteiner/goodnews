import time
from news import generate_news
import telebot
import os
from dotenv import load_dotenv
import datetime
import random

load_dotenv()

bot = telebot.TeleBot(os.environ['GUTE_NACHTICHTEN_TELEGRAM_BOT_TOKEN'])

CHANNEL_ID = os.environ['GUTE_NACHTICHTEN_TELEGRAM_CHANNEL_ID']

def send_news():
    # Generate a random news message
    news = generate_news()

    # Send the news message to the channel
    bot.send_message(CHANNEL_ID, news)

if __name__ == "__main__":
    send_news()
    
