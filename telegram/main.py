import telebot
import datetime
import os
import asyncio
from jinja2 import Environment, FileSystemLoader
import random

from utils.reader import reader
from utils.preprocesser import sort_by
from utils.ranker import ranker

rate_limiter = asyncio.Semaphore(20)
FILEPATH = './data.json'
today = str(datetime.datetime.today().strftime('%Y-%m-%d'))

# Get Telegram bot token and chat ID
bot_token = os.getenv('TELEGRAM_TOKEN')
chat_id = os.getenv('TELEGRAM_CHANNEL')

# Create a Telegram bot instance
bot = telebot.TeleBot(bot_token)

# Function to send a message
async def send_message(message):
    async with rate_limiter:
        try:
            if len(message) > 4095:
                for x in range(0, len(message), 4095):
                    bot.send_message(chat_id, message[x:x+4095])
            else:
                bot.send_message(chat_id, message)
            print("Message sent successfully!")
        except telebot.apihelper.ApiTelegramException as e:
            if e.error_code == 429:  # Rate limit exceeded
                wait_time = random.randint(1, 60)  # Wait for 1 to 60 seconds
                print(f"Rate limit exceeded. Waiting {wait_time} seconds...")
                await asyncio.sleep(wait_time)
                await send_message(message)  # Retry the request
            else:
                raise e

# Example usage
if __name__ == "__main__":
    data = reader(FILEPATH)
    data = ranker(data, threshold=0)
    data = sort_by(data)

    env = Environment(loader=FileSystemLoader('templates'))

    xResume = env.get_template('notePost.j2')
    resume_page = xResume.render(today=today)
    if data != []:
        asyncio.run(send_message(resume_page))

    types = set([x['type'] for x in data])
    for t in types:
        xPostTemplate = env.get_template('head.j2')
        head = xPostTemplate.render(today=today, type=t)
        asyncio.run(send_message(head))
        for x in data:
            if t == x['type']:
                xPostTemplate = env.get_template('post.j2')
                post = xPostTemplate.render(publication=x, today=today, type=x['type'])
                asyncio.run(send_message(post))
