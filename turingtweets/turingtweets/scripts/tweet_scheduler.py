import schedule
import tweepy
import api_keys


def job(tweet):
    auth = tweepy.OAuthHandler(api_keys.consumer_key, api_keys.consumer_secret)
    auth.set_access_token(api_keys.access_token, api_keys.access_token_secret)

    api = tweepy.API(auth)
    api.update_status(status=tweet)