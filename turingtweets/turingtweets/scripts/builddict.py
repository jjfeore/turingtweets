"""Use NLTK to build an N-grams dictionary out of the tweets."""


import markovify
import redis
import pickle
import os
import logging
from turingtweets.models import get_engine
from sqlalchemy.orm import sessionmaker
from turingtweets.models.mymodel import Tweet


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
