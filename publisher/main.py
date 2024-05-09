import datetime
import tweepy
import os
import json

## URLOCK
import urlock
import time

from jinja2 import Environment, FileSystemLoader

from utils.reader import reader
from utils.preprocesser import sort_by
from utils.ranker import ranker


FILEPATH = './data.json'
TWEET_MAX_LENGTH = 327

today = str(datetime.datetime.today().strftime('%Y-%m-%d'))
# today = str(datetime.datetime(2023, 12, 22).strftime('%Y-%m-%d'))


def main():
    data = reader(FILEPATH)
    data = ranker(data, threshold=0) #date= datetime.datetime(2023, 12, 22).date())
    data = sort_by(data)
    env = Environment(loader=FileSystemLoader('templates'))


    # Validate Length 
    exceeded = False
    for x in data:
        if len(x['summary']) > 280:
            print(x)
            exceeded = True
    
    if exceeded:
        return True


    # Urbit
    ship = urlock.Urlock(os.getenv('URBIT_SHIP_URL'), os.getenv('URBIT_SHIP_CODE'))
    r = ship.connect()

    shipName = os.getenv('URBIT_SHIP')
    diary = os.getenv('URBIT_DIARY')

    template = env.get_template('note.j2')
    rendered_note = template.render(results=data, today=today, types=set([x['type'] for x in data]), nest="diary/~" + shipName + "/" + diary, ship="~" + shipName, time=int(time.time() * 1000))
    note = json.loads(rendered_note)
    ship.poke(shipName, "channels", "channel-action", note)


    # X

    client = tweepy.Client(bearer_token=os.getenv('X_BEARER'), consumer_key=os.getenv('X_API_KEY'), consumer_secret=os.getenv('X_API_KEY_SECRET'), access_token=os.getenv('X_ACCESS_TOKEN'), access_token_secret=os.getenv('X_ACCESS_TOKEN_SECRET'), wait_on_rate_limit=True)

    xResume = env.get_template('notePost.j2')
    resume_tweet = xResume.render(today=today)
    client.create_tweet(text=resume_tweet)

    types = set([x['type'] for x in data])
    for t in types:
        xPostTemplate = env.get_template('head.j2')
        tweet = xPostTemplate.render(today=today, type=t)
        original_tweet = client.create_tweet(text=tweet)
        for x in data:
            if t == x['type']:
                xPostTemplate = env.get_template('post.j2')
                tweet = xPostTemplate.render(publication=x, today=today, type=x['type'])
                if len(tweet) > TWEET_MAX_LENGTH:
                    xPostTemplate = env.get_template('area.j2')
                    area = xPostTemplate.render(publication=x, today=today, type=x['type'])
                    reply_tweet = client.create_tweet(text=area, 
                                            in_reply_to_tweet_id=original_tweet.data['id'])
                    xPostTemplate = env.get_template('summary.j2')
                    summary = xPostTemplate.render(publication=x, today=today, type=x['type'])
                    reply2_tweet = client.create_tweet(text=summary, 
                                                in_reply_to_tweet_id=reply_tweet.data['id'])
                    original_tweet = reply2_tweet
                else:   
                    reply_tweet = client.create_tweet(text=tweet, 
                                                in_reply_to_tweet_id=original_tweet.data['id'])
                    original_tweet = reply_tweet

if __name__ == "__main__":
    main()