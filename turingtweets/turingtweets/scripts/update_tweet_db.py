import os
import datetime
import tweepy
import markovify
import redis
import pickle

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import MetaData

from sqlalchemy import (
    Column,
    Unicode,
    Integer,
    Boolean,
)


from sqlalchemy import engine_from_config
# from turingtweets.models import get_engine
from sqlalchemy.orm import sessionmaker


def gen_markov():
    """Compile all the tweets and create a Markov chain."""
    host_url = os.environ.get('REDIS_URL')
    access_dict = {'sqlalchemy.url': os.environ.get('DATABASE_URL')}
    engine = get_engine(access_dict)
    SessionFactory = sessionmaker(bind=engine)
    session = SessionFactory()

    tweets = session.query(Tweet).all()

    big_corpus = ''
    for tweet in tweets:
        big_corpus += tweet.tweet + '\n'
    markov_chain = markovify.NewlineText(big_corpus, state_size=3)
    to_redis = pickle.dumps(markov_chain)
    redis.from_url(host_url).set('markov_tweets', to_redis)


NAMING_CONVENTION = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=NAMING_CONVENTION)
Base = declarative_base(metadata=metadata)


class Tweet(Base):
    """Model for a single tweet."""

    __tablename__ = 'tweets'
    id = Column(Integer, primary_key=True)
    tweet = Column(Unicode)



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
