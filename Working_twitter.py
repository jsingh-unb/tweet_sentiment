

import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob


class TwitterAccess(object):

    def __init__(self):
        consumer_key = 'XYZ'
        consumer_secret = 'XYZ'
        access_token = 'XYZ'
        access_token_secret = 'XYZ'
        try:
            auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
            auth.set_access_token(access_token, access_token_secret)
            self.api = tweepy.API(auth)
        except:
            print("Error: Wrong credentials")

    def clean_tweet(self, tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) |(\w+:\/\/\S+)", " ", tweet).split())

    def get_tweet_sentiment(self, tweet):
        analysis = TextBlob(self.clean_tweet(tweet))
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity ==0:
            return 'neutral'
        else:
            return 'negative'

    def get_tweets(self, query, count):
        tweets = []

        try:
            fetched_tweets = self.api.search(q=query, count=count)
            for tweet in fetched_tweets:
                parsed_tweet = {}

                parsed_tweet['text'] = tweet.text
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)

                if tweet.retweet_count > 0:
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)
            return tweets
        except tweepy.TweepError as e:
            print("Error : " + str(e))


def main():

    classobj = TwitterAccess()

    tweets = classobj.get_tweets(query="@IndiavsPak", count=2000)
    ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
    print("Positive tweets percentage: {} %".format(100 * len(ptweets) / len(tweets)))
    ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
    print("Negative tweets percentage: {} %".format(100 * len(ntweets) / len(tweets)))
    neutweets = [tweet for tweet in tweets if tweet['sentiment'] == 'neutral']

    print("Neutral tweets percentage: {} %".format(100*(len(neutweets)/len(tweets))))

    print("\n\nPositive tweets:")
    for tweet in ptweets[:10]:
        print(tweet['text'])

    print("\n\nNegative tweets:")
    for tweet in ntweets[:10]:
        print(tweet['text'])

    print('\n\nNeutral tweets:')
    for tweet in neutweets[:10]:
        print(tweet['text'])



if __name__ == "__main__":
    # calling main function
    main()


















