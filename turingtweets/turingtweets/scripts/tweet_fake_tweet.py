import os
import tweepy
from turingtweets.models import get_engine
from sqlalchemy.orm import sessionmaker
from turingtweets.models.mymodel import FakeTweet

# MAKE SURE IT DOESN'T CRASH WHEN FAKE TWEET DB IS EMPTY


def get_fake_tweet():
    test_dict = {'sqlalchemy.url': os.environ.get('DATABASE_URL')}
    print(os.environ.get('DATABASE_URL'))
    engine = get_engine(test_dict)
    print(engine)
    SessionFactory = sessionmaker(bind=engine)
    session = SessionFactory()
    fake_tweet = session.query(FakeTweet).filter_by(tweeted=False).first().faketweet
    session.query(FakeTweet).filter(FakeTweet.faketweet == fake_tweet).update({'tweeted':True})
    session.commit()
    print(fake_tweet)
    return fake_tweet


def tweet_fake_tweet(tweet):
    auth = tweepy.OAuthHandler(os.environ.get('CONSUMER_KEY'), os.environ.get('CONSUMER_SECRET'))
    auth.set_access_token(os.environ.get('ACCESS_TOKEN'), os.environ.get('ACCESS_TOKEN_SECRET'))
    api = tweepy.API(auth)
    api.update_status(status=tweet)


tweet_fake_tweet(get_fake_tweet())