import os
import datetime
import tweepy
from sqlalchemy import engine_from_config
# from turingtweets.models import get_engine
from sqlalchemy.orm import sessionmaker
from turingtweets.models.mymodel import Tweet
from turingtweets.scripts.builddict import gen_markov


def get_engine(settings, prefix='sqlalchemy.'):
    return engine_from_config(settings, prefix)


def update_tweet_db():
    """
    This function updates the database with tweets from the last 24 hours.
    """
    test_dict = {'sqlalchemy.url': os.environ.get('DATABASE_URL')}
    engine = get_engine(test_dict)
    SessionFactory = sessionmaker(bind=engine)
    session = SessionFactory()
    api = authenticate_with_twitter()
    list_of_tweets = get_tweets(api, "realdonaldtrump")
    tweet_objects = []
    for tweet in list_of_tweets:
        tweet_objects.append(Tweet(tweet=tweet))
    session.add_all(tweet_objects)
    session.commit()
    gen_markov()


def authenticate_with_twitter():
    """
    This function is responsible for authenticating with Twitter.
    """
    auth = tweepy.OAuthHandler(os.environ.get('CONSUMER_KEY'), os.environ.get('CONSUMER_SECRET'))
    auth.set_access_token(os.environ.get('ACCESS_TOKEN'), os.environ.get('ACCESS_TOKEN_SECRET'))
    api = tweepy.API(auth)
    return api


def get_tweets(api, username):
    """
    This function is responsible for getting tweets from the last 24 hours.
    """
    tweets = api.user_timeline(username, page=1)
    list_of_tweets = []
    for tweet in tweets:
        if (datetime.datetime.now() - tweet.created_at).days < 1:
            list_of_tweets.append(tweet.text)
    return list_of_tweets


if __name__ == "__main__":
    update_tweet_db()
