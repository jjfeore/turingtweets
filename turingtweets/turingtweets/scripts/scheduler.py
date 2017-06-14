from apscheduler.schedulers.blocking import BlockingScheduler
from turingtweets.scripts.tweet_fake_tweet import get_fake_tweet, tweet_fake_tweet
import logging

sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=1)
def timed_job():
    logging.exception('THIS JOB IS RUN EVERY MINUTE.')


sched.start()