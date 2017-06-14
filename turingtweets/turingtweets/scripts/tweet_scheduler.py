# import schedule
# import tweepy
# import api_keys
# import time
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


print("dbsession result: {}".format(session.query(FakeTweet).filter_by(tweeted=False).first().faketweet))


# def job(tweet):
#     auth = tweepy.OAuthHandler(api_keys.consumer_key, api_keys.consumer_secret)
#     auth.set_access_token(api_keys.access_token, api_keys.access_token_secret)
#     api = tweepy.API(auth)
#     api.update_status(status=tweet)
#
#
# schedule.every().hour.do(job)

# while True:
#     print("Inside of tweet_scheduler:")
#     schedule.run_pending()
#     time.sleep(1)

