import json
import threading
import time

import settings
import sharedData
from twitternews.lastNews import TwitterNews


class TweetNewsProvider(threading.Thread):
    lastTimeUpdated = 0
    delayForRequests = 60  # in seconds (5 min)

    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True

    def run(self):
        while True:
            try:
                self.requestData()
            except Exception as err:
                print(f"TweetNewsProvider Error :{err.__str__()}")
            time.sleep(25)

    def requestData(self):
        with open(settings.pathToTwitterAccounts, mode='r') as file:
            twitterAccounts = json.load(file).get('accounts')
            if twitterAccounts:
                if (time.time() - self.lastTimeUpdated) > self.delayForRequests:
                    self.lastTimeUpdated = time.time()
                    sharedData.tweets.value.clear()
                    tweets = TwitterNews.getTweetsFrom(twitterAccounts)
                    sharedData.tweets.value.extend(tweets)
                    sharedData.tweets.changed.emit()
