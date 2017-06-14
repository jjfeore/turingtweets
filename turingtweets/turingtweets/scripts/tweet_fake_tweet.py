import os
import tweepy
from turingtweets.models import get_engine
from sqlalchemy.orm import sessionmaker
from turingtweets.models.mymodel import FakeTweet


def get_fake_tweet():
    test_dict = {'sqlalchemy.url': os.environ.get('DATABASE_URL')}
    engine = get_engine(test_dict)
    SessionFactory = sessionmaker(bind=engine)
    session = SessionFactory()
    if session.query(FakeTweet).filter_by(tweeted=False).first():
        print('we have a tweet to tweet.')
        fake_tweet = session.query(FakeTweet).filter_by(tweeted=False).first().faketweet
        session.query(FakeTweet).filter(FakeTweet.faketweet == fake_tweet).update({'tweeted':True})
        session.commit()
        print(fake_tweet)
        tweet_fake_tweet(fake_tweet)


def tweet_fake_tweet(tweet):
    auth = tweepy.OAuthHandler(os.environ.get('CONSUMER_KEY'), os.environ.get('CONSUMER_SECRET'))
    auth.set_access_token(os.environ.get('ACCESS_TOKEN'), os.environ.get('ACCESS_TOKEN_SECRET'))
    api = tweepy.API(auth)
    api.update_status(status=tweet)


if __name__ == "__main__":
    get_fake_tweet()
