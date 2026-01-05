import datetime
import os
import json

## URLOCK
import urlock
import time

from jinja2 import Environment, FileSystemLoader
from xdk import Client
from xdk.oauth1_auth import OAuth1

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

    # X
    oauth1 = OAuth1(
        api_key=os.getenv('X_API_KEY'),
        api_secret=os.getenv('X_API_KEY_SECRET'),
        access_token=os.getenv('X_ACCESS_TOKEN'),
        access_token_secret=os.getenv('X_ACCESS_TOKEN_SECRET')
    )
    client = Client(auth=oauth1)

    types = set([x['type'] for x in data])
    for t in types:
        xPostTemplate = env.get_template('head.j2')
        tweet = xPostTemplate.render(today=today, type=t)
        original_tweet = client.posts.create(body={"text": tweet})
        for x in data:
            if t == x['type']:
                xPostTemplate = env.get_template('post.j2')
                tweet = xPostTemplate.render(publication=x, today=today, type=x['type'])
                if len(tweet) > TWEET_MAX_LENGTH:
                    xPostTemplate = env.get_template('area.j2')
                    area = xPostTemplate.render(publication=x, today=today, type=x['type'])
                    reply_tweet = client.posts.create(body={"text": area}, reply={"in_reply_to_post_id": original_tweet.data['id']})
                    xPostTemplate = env.get_template('summary.j2')
                    summary = xPostTemplate.render(publication=x, today=today, type=x['type'])
                    reply2_tweet = client.posts.create(body={"text": summary}, reply={"in_reply_to_post_id": reply_tweet.data['id']})
                    original_tweet = reply2_tweet
                else:   
                    reply_tweet = client.posts.create(body={"text": tweet}, reply={"in_reply_to_post_id": original_tweet.data['id']})
                    original_tweet = reply_tweet


if __name__ == "__main__":
    main()