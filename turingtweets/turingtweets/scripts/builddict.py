"""Use NLTK to build an N-grams dictionary out of the tweets."""


import markovify
import redis
import pickle
import os
import logging


def fourgrams(tweets):
    """Add a dictionary of Markov chains to the models."""
    host_url = os.environ.get('REDIS_URL')
    markov_list = []
    for tweet in tweets:
        try:
            markov_list.append(markovify.Text(tweet, state_size=2))
        except Exception:
            logging.exception('Markov doesn\'t like parens or quotes')
            pass
    markov_list = markovify.combine(markov_list)
    to_redis = pickle.dumps(markov_list)
    redis.StrictRedis(host=host_url).set('markov_tweets', to_redis)
