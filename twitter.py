import json
import tweepy


class Twitter:

    def __init__(self, config_file: str):
        with open(config_file, 'r') as f:
            data = f.read()

        settings = json.loads(data)

        self.consumer_key = settings['twitterApiKey']
        self.consumer_secret = settings['twitterSecretKey']

        self.auth = tweepy.AppAuthHandler(self.consumer_key, self.consumer_secret)
        self.api = tweepy.API(self.auth)

    def get_tweets_from_user(self, user_handle: str):
        return self.api.user_timeline(screen_name=user_handle)

    def get_tweets_from_user_since(self, user_handle: str, since_id: int):
        return self.api.user_timeline(screen_name=user_handle, since_id=since_id)
