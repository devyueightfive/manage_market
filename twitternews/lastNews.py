import twitter


class TwitterNews:
    consumerKey, \
    consumerSecret, \
    accessTokenKey, \
    accessTokenSecret = ('v6FJlVKZISs70wpsRqTJUGoXL',
                         'jLV26iP0PNzdl6IkHiRNJFmPa2HD2SPW6otcUFzvZFHluLnWas',
                         '990221247152783361-ESxBNj1oCiHAVLJlaJyrMlMqQKyepuT',
                         'YwtbFRTTqa1SiXm7GyszwSLIBIESPs925HfAOcmRgad1U')

    @staticmethod
    def getTweetsFrom(users: list) -> list:
        twitterAPI = twitter.Api(TwitterNews.consumerKey,
                                 TwitterNews.consumerSecret,
                                 TwitterNews.accessTokenKey,
                                 TwitterNews.accessTokenSecret)
        listOfTweets = []
        setOfIDs = set()
        for user in users:
            try:
                results = twitterAPI.GetUserTimeline(screen_name=user, count=10, exclude_replies=True)
                for status in results:
                    status = status.AsDict()
                    tweet = {'screen_name': status['user']['screen_name'],
                             'profile_image_url': status['user']['profile_image_url'],
                             'created_at': status['created_at'],
                             'id': status['id'],
                             'text': status['text'],
                             'url': f'https://twitter.com/i/web/status/{str(status["id"])}'}
                    if tweet['id'] not in setOfIDs:
                        listOfTweets.append(tweet)
                    setOfIDs.add(tweet['id'])
            except Exception as err:
                print(f'{user}:{err}')
        return sorted(listOfTweets, key=lambda x: x['id'], reverse=True)
