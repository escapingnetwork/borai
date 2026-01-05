import datetime
import os
import json

## URLOCK
import urlock
import time

from jinja2 import Environment, FileSystemLoader
from xai_sdk import Client

from utils.reader import reader
from utils.preprocesser import sort_by
from utils.ranker import ranker


FILEPATH = './data.json'
TWEET_MAX_LENGTH = 327

today = str(datetime.datetime.today().strftime('%Y-%m-%d'))
#today = str(datetime.datetime(2025, 12, 9).strftime('%Y-%m-%d'))


def main():
    data = reader(FILEPATH)
    data = ranker(data, threshold=0) #, date=datetime.datetime(2025, 12, 9).date())
    data = sort_by(data)
    env = Environment(loader=FileSystemLoader('templates'))


    # Validate Length 
    # exceeded = False
    # for x in data:
    #     if len(x['summary']) > 280:
    #         print(x)
    #         exceeded = True
    
    # if exceeded:
    #     return True


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
    client = Client(api_key=os.getenv('X_API_KEY'))
    
    xResume = env.get_template('notePost.j2')
    resume_tweet = xResume.render(today=today)
    client.post(resume_tweet)

if __name__ == "__main__":
    main()