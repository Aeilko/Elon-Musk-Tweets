from datetime import datetime
from notify_run import Notify
from twitter import Twitter

import os
import sys
import json


CONFIG_FILE = "settings.json"
PROJECT_SETTINGS = None
BASE_DIR = os.path.dirname(__file__)

def check_for_tweets():
    twitter = Twitter(os.path.join(BASE_DIR, CONFIG_FILE))

    try:
        # Check which tweets have already been processed
        with open(os.path.join(BASE_DIR, "prev_id"), "r") as file:
            prev_id = int(file.read())
    except FileNotFoundError:
        # File 'prev_id' does not exist, set it as his most recent tweet
        tweets = twitter.get_tweets_from_user(PROJECT_SETTINGS['elonHandle'])
        prev_id = tweets[0].id


    # Load the keywords we are checking for
    with open(os.path.join(BASE_DIR, "keywords"), "r") as file:
        keys = file.read()
    keywords = keys.split("\n")

    # Load tweets
    tweets = twitter.get_tweets_from_user_since(PROJECT_SETTINGS['elonHandle'], prev_id)

    # Check the tweets for keywords
    found = set()
    max_id = prev_id
    for tweet in tweets:
        id = tweet.id
        txt = str(tweet.text).lower()
        for key in keywords:
            if key in txt:
                found.add(key)
        if id > max_id:
            max_id = id

    # Save our progress
    with open(os.path.join(BASE_DIR, "prev_id"), "w") as file:
        file.write(str(max_id))

    # Notify if necessary
    if len(found) > 0:
        msg = "Elon Tweeted about the following topics: '" + ", ".join(found) + "'"

        notify = Notify()
        if notify.config_file_exists:
            notify.read_config()
        else:
            print(notify.register())
            notify.write_config()

        print("[" + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + "] Sending notification: " + msg)

        notify.send(msg, "https://www.twitter.com/" + PROJECT_SETTINGS['elonHandle'])


if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == "info":
        notify = Notify()
        notify.read_config()
        print(notify.info())
    else:
        with open(os.path.join(BASE_DIR, CONFIG_FILE), 'r') as f:
            data = f.read()

        PROJECT_SETTINGS = json.loads(data)

        check_for_tweets()
