# Elon Musk Tweets

### Installation
Install [Notify.run](https://github.com/notify-run/notify.run) ``pip install notify-run``

Install [Tweepy](https://github.com/tweepy/) ``pip install tweepy``

### Configure
Copy/rename the settings file.

Register a [Twitter App](https://developer.twitter.com/) and set the API key and Secret Key in the settings  file.

### First run
Run it using "info" parameter, then scan the QR code and register for notifications.

```python check_for_tweet.py info```

### Cronjob

``*/2 * * * * /usr/bin/python3 /home/.../check_for_tweet.py >> /home/.../log/cron 2>&1``