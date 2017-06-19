import os
import tweepy
from sqlalchemy import (
    Column,
    Unicode,
    Integer,
    Boolean,
)


from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import MetaData


from sqlalchemy import engine_from_config
from sqlalchemy.orm import sessionmaker


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


class FakeTweet(Base):
    """Model for a single fake tweet."""
    __tablename__ = 'fake-tweets'
    id = Column(Integer, primary_key=True)
    faketweet = Column(Unicode)
    tweeted = Column(Boolean)
    shown = Column(Integer)
    chosen = Column(Integer)


def get_engine(settings, prefix='sqlalchemy.'):  # pragma: no cover
    return engine_from_config(settings, prefix)


def get_fake_tweet():
    test_dict = {'sqlalchemy.url': os.environ.get('DATABASE_URL')}
    engine = get_engine(test_dict)
    SessionFactory = sessionmaker(bind=engine)
    session = SessionFactory()
    if session.query(FakeTweet).filter_by(tweeted=False).first():
        fake_tweet = session.query(FakeTweet).filter_by(tweeted=False).first().faketweet
        session.query(FakeTweet).filter(FakeTweet.faketweet == fake_tweet).update({'tweeted':True})
        session.commit()
        tweet_fake_tweet(fake_tweet)


def tweet_fake_tweet(tweet):  # pragma: no cover
    auth = tweepy.OAuthHandler(os.environ.get('CONSUMER_KEY'), os.environ.get('CONSUMER_SECRET'))
    auth.set_access_token(os.environ.get('ACCESS_TOKEN'), os.environ.get('ACCESS_TOKEN_SECRET'))
    api = tweepy.API(auth)
    api.update_status(status=tweet)


if __name__ == "__main__":  # pragma: no cover
    print('running tweet_fake_tweet...')
    get_fake_tweet()
