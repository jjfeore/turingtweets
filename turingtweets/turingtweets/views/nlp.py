"""Use NLP to generate fake tweets."""


import markovify
import redis
import pickle
import os


def gen_tweet():
    """Read the redis, and build a fake tweet from that."""
    host_url = os.environ.get('REDIS_URL')
    chains = redis.from_url(host_url)
    markov_chains = chains.get('markov_tweets')
    markov_chains = pickle.loads(markov_chains)
    the_tweet = None

    while not the_tweet:
        the_tweet = markov_chains.make_short_sentence(140, 70)
    return the_tweet
