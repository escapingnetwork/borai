import datetime
import tweepy
import os
import json
import urlock
import time
import logging

from jinja2 import Environment, FileSystemLoader
from utils.reader import reader
from utils.preprocesser import sort_by
from utils.ranker import ranker

FILEPATH = './data.json'
TWEET_MAX_LENGTH_WITH_LINK = 327
TWEET_MAX_LENGTH = 280

today = str(datetime.datetime.today().strftime('%Y-%m-%d'))

def validate_length(data):
    exceeded = False
    for entry in data:
        if len(entry['summary']) > TWEET_MAX_LENGTH:
            logging.warning(f"Summary exceeded 280 characters: {entry}")
            exceeded = True
    return exceeded

def main():
    """
    This is the main function that executes the publishing process.

    It reads data from a file, ranks the data, sorts it, connects to an Urbit ship,
    renders templates, creates tweets, and publishes them.

    Returns:
        None
    """
    data = reader(FILEPATH)
    data = ranker(data, threshold=0)
    data = sort_by(data)
    env = Environment(loader=FileSystemLoader('templates'))

    if validate_length(data):
        return

    ship = urlock.Urlock(os.getenv('URBIT_SHIP_URL'), os.getenv('URBIT_SHIP_CODE'))
    connection_status = ship.connect()

    ship_name = os.getenv('URBIT_SHIP')
    diary = os.getenv('URBIT_DIARY')

    templates = {
        'note': env.get_template('note.j2'),
        'head': env.get_template('head.j2'),
        'post': env.get_template('post.j2'),
        'area': env.get_template('area.j2'),
        'summary': env.get_template('summary.j2')
    }

    rendered_note = templates['note'].render(results=data, today=today, types=set([entry['type'] for entry in data]), nest=f"diary/~{ship_name}/{diary}", ship=f"~{ship_name}", time=int(time.time() * 1000))
    note = json.loads(rendered_note)
    poke_response = ship.poke(ship_name, "channels", "channel-action", note)

    client = tweepy.Client(bearer_token=os.getenv('X_BEARER'), consumer_key=os.getenv('X_API_KEY'), consumer_secret=os.getenv('X_API_KEY_SECRET'), access_token=os.getenv('X_ACCESS_TOKEN'), access_token_secret=os.getenv('X_ACCESS_TOKEN_SECRET'), wait_on_rate_limit=True)

    types = set([entry['type'] for entry in data])
    for type in types:
        tweet_text = templates['head'].render(today=today, type=type)
        original_tweet = client.create_tweet(text=tweet_text)
        for entry in data:
            if type == entry['type']:
                tweet_text = templates['post'].render(publication=entry, today=today, type=entry['type'])
                if len(tweet_text) > TWEET_MAX_LENGTH_WITH_LINK:
                    area_text = templates['area'].render(publication=entry, today=today, type=entry['type'])
                    reply_tweet = client.create_tweet(text=area_text, in_reply_to_tweet_id=original_tweet.data['id'])
                    summary_text = templates['summary'].render(publication=entry, today=today, type=entry['type'])
                    reply2_tweet = client.create_tweet(text=summary_text, in_reply_to_tweet_id=reply_tweet.data['id'])
                    original_tweet = reply2_tweet
                else:   
                    reply_tweet = client.create_tweet(text=tweet_text, in_reply_to_tweet_id=original_tweet.data['id'])
                    original_tweet = reply_tweet

if __name__ == "__main__":
    main()