import schedule
import tweepy
import time
import os
from turingtweets.scripts.tweet_fake_tweet import get_fake_tweet, tweet_fake_tweet
from turingtweets.scripts.update_tweet_db import <FUNCTIONS TO IMPORT>


############### SCHEDULE TEMPLATE ##############
# def job():
#     print("I'm working...")
#
# schedule.every().hour.do(job)
# schedule.every().day.at("10:30").do(job)
# schedule.every().monday.do(job)
# schedule.every().wednesday.at("13:15").do(job)
#
# while True:
#     schedule.run_pending()
#     time.sleep(1)
