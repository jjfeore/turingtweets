"""Define the routes."""


from pyramid.response import Response
from pyramid.view import view_config
from sqlalchemy.exc import DBAPIError
from turingtweets.models import mymodel
from ..models import Tweet
from pyramid.httpexceptions import (
    HTTPNotFound,
    HTTPFound
)
import random
from turingtweets.views.nlp import gen_tweet


@view_config(route_name='home', renderer='../templates/mytemplate.jinja2')
def home_view(request):
    """View for home route."""
    session = request.dbsession
    tweet_ct = session.query(Tweet).count()
    rand_tweet = random.randint(1, tweet_ct)
    real_tweet = session.query(Tweet).get(rand_tweet)
    fake_tweet = gen_tweet()
    return {
        'page': 'Home',
        'real': real_tweet.tweet,
        'fake': fake_tweet
    }
