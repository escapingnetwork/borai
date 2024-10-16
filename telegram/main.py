import telebot
import datetime
import os
from jinja2 import Environment, FileSystemLoader

from utils.reader import reader
from utils.preprocesser import sort_by
from utils.ranker import ranker


FILEPATH = './data.json'
today = str(datetime.datetime.today().strftime('%Y-%m-%d'))

# Get Telegram bot token and chat ID
bot_token = os.getenv('TELEGRAM_TOKEN')
chat_id = os.getenv('TELEGRAM_CHANNEL')

# Create a Telegram bot instance
bot = telebot.TeleBot(bot_token)

# Function to send a message
def send_message(message):
    try:
        bot.send_message(chat_id, message)
        print("Message sent successfully!")
    except Exception as e:
        print("Error sending message:", str(e))

# Example usage
if __name__ == "__main__":
    data = reader(FILEPATH)
    data = ranker(data, threshold=0)
    data = sort_by(data)

    env = Environment(loader=FileSystemLoader('templates'))

    xResume = env.get_template('notePost.j2')
    resume_page = xResume.render(today=today)
    send_message(resume_page)

    types = set([x['type'] for x in data])
    for t in types:
        xPostTemplate = env.get_template('head.j2')
        head = xPostTemplate.render(today=today, type=t)
        send_message(head)
        for x in data:
            if t == x['type']:
                xPostTemplate = env.get_template('post.j2')
                post = xPostTemplate.render(publication=x, today=today, type=x['type'])
                send_message(post)
