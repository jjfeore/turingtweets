"""Define the routes."""


from pyramid.response import Response
from pyramid.view import view_config
from sqlalchemy.exc import DBAPIError
from turingtweets.models import mymodel
from turingtweets.models.mymodel import Tweet, FakeTweet
from pyramid.httpexceptions import HTTPNotFound
from turingtweets.views.nlp import gen_tweet
from sqlalchemy.sql.expression import func


@view_config(route_name='home', renderer='../templates/mytemplate.jinja2')
def home_view(request):
    """View for home route."""
    session = request.dbsession
    real_tweet = session.query(Tweet).order_by(func.random()).first()
    fake_tweet = gen_tweet()
    if request.method == "POST" and request.POST:
        new_entry = FakeTweet(
            faketweet=request.POST['fakeTweet'],
            tweeted=False,
            shown=1,
            chosen=1
        )
        request.dbsession.add(new_entry)
        return {}
    return {
        'page': 'Home',
        'real': real_tweet.tweet,
        'fake': fake_tweet
    }


@view_config(route_name='documentation', renderer='../templates/documentation.jinja2')
def doc_view(request):
    """View for documentation route."""
    return {
        'page': 'Documentation'
    }


@view_config(route_name='about', renderer='../templates/about.jinja2')
def about_view(request):
    """View for about route."""
    return {
        'page': 'About the Team'
    }


@view_config(route_name='json-fake', renderer='json')
def json_fake(request):
    """Return a JSON with a fake tweet."""
    return {
        'tweet': gen_tweet()
    }


@view_config(route_name='json-real', renderer='json')
def json_real(request):
    """Return a JSON with a random real tweet."""
    session = request.dbsession
    real_tweet = session.query(Tweet).order_by(func.random()).first()
    return {
        'tweet': real_tweet.tweet
    }


@view_config(route_name='json-fake-validated', renderer='json')
def json_fake_validated(request):
    """Return a JSON with a random user-validated, fake tweet."""
    session = request.dbsession
    if session.query(FakeTweet).first():
        fake_tweet = session.query(FakeTweet).order_by(func.random()).first()
        return {
            'tweet': fake_tweet.faketweet
        }
    else:
        return {}
