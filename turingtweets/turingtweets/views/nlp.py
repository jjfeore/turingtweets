"""Use NLP to generate fake tweets."""


import markovify
import redis
import pickle
import os


def gen_tweet():
    """Read the redis, and build a fake tweet from that."""
    host_url = os.environ.get('REDIS_URL')
    markov_chains = redis.StrictRedis(host=host_url).get('markov_tweets')
    markov_chains = pickle.loads(markov_chains)
    return markov_chains.make_short_sentence(140)
