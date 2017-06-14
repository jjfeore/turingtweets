import schedule
import tweepy
import time
import os


from turingtweets.models import get_engine
from sqlalchemy.orm import sessionmaker
from turingtweets.models.mymodel import FakeTweet

test_dict = {'sqlalchemy.url': os.environ.get('DATABASE_URL')}
print(os.environ.get('DATABASE_URL'))
engine = get_engine(test_dict)
print(engine)
SessionFactory = sessionmaker(bind=engine)
session = SessionFactory()


faketweet = session.query(FakeTweet).filter_by(tweeted=False).first().faketweet


def job(tweet):
    auth = tweepy.OAuthHandler(os.environ.get('CONSUMER_KEY'), os.environ.get('CONSUMER_SECRET'))
    auth.set_access_token(os.environ.get('ACCESS_TOKEN'), os.environ.get('ACCESS_TOKEN_SECRET'))
    api = tweepy.API(auth)
    api.update_status(status=tweet)


# schedule.every().hour.do(job)
job(faketweet)

# while True:
#     print("Inside of tweet_scheduler:")
#     schedule.run_pending()
#     time.sleep(1)

