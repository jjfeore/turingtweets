import os
import datetime
import tweepy
from turingtweets.models import get_engine
from sqlalchemy.orm import sessionmaker
from turingtweets.models.mymodel import FakeTweet


def update_tweet_db():
    test_dict = {'sqlalchemy.url': os.environ.get('DATABASE_URL')}
    print(os.environ.get('DATABASE_URL'))
    engine = get_engine(test_dict)
    print(engine)
    SessionFactory = sessionmaker(bind=engine)
    session = SessionFactory()
    api = authenticate_with_twitter()
    list_of_tweets = get_tweets(api, "nhuntwalker")
    print(list_of_tweets)
    for tweet in list_of_tweets:
        print("Inside of update_tweet_db: {}".format(tweet))


def authenticate_with_twitter():
    auth = tweepy.OAuthHandler(os.environ.get('CONSUMER_KEY'), os.environ.get('CONSUMER_SECRET'))
    auth.set_access_token(os.environ.get('ACCESS_TOKEN'), os.environ.get('ACCESS_TOKEN_SECRET'))
    api = tweepy.API(auth)
    return api


def get_tweets(api, username):
    tweets = api.user_timeline(username, page=1)
    list_of_tweets = []
    for tweet in tweets:
        if (datetime.datetime.now() - tweet.created_at).days < 1:
            list_of_tweets.append(tweet.text)
    return list_of_tweets


update_tweet_db()