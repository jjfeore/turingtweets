from apscheduler.schedulers.blocking import BlockingScheduler
from turingtweets.scripts.tweet_fake_tweet import get_fake_tweet, tweet_fake_tweet

sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=1)
def timed_job():
    print('This job is run every minute.')


sched.start()