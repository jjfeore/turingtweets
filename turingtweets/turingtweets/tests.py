"""Test for turingtweets."""
import pytest
import os
import json
from pyramid import testing
from pyramid.response import Response
from turingtweets.models.mymodel import Tweet, FakeTweet
from pyramid.httpexceptions import HTTPNotFound
from turingtweets.models.meta import Base
from turingtweets.models import get_engine
from sqlalchemy.orm import sessionmaker

SITE_ROOT = 'http://localhost'


@pytest.fixture(scope="session")
def configuration(request):
    """Set up a configurator instance."""
    config = testing.setUp(settings={
        'sqlalchemy.url': os.environ.get('DATABASE_URL_TESTING')
    })
    config.include("turingtweets.models")
    config.include("turingtweets.routes")

    def teardown():
        testing.tearDown()

    request.addfinalizer(teardown)
    return config


@pytest.fixture
def db_session(configuration, request):
    """Create a session for interacting with the test database."""
    session_factory = configuration.registry["dbsession_factory"]
    session = session_factory()
    engine = session.bind
    Base.metadata.create_all(engine)
    a_tweet = Tweet(tweet='poop')
    session.add(a_tweet)

    def teardown():
        session.transaction.rollback()
        Base.metadata.drop_all(engine)

    request.addfinalizer(teardown)
    return session


@pytest.fixture
def dummy_request(db_session):
    """Create a dummy request."""
    from pyramid import testing
    req = testing.DummyRequest()
    req.dbsession = db_session
    return req


@pytest.fixture
def post_request(dummy_request):
    """Create a dummy post request."""
    dummy_request.method = "POST"
    return dummy_request


@pytest.fixture
def testapp_route():
    """Create a test application to use for functional tests."""
    from turingtweets import main
    from webtest import TestApp
    app = main({})
    return TestApp(app)


@pytest.fixture(scope='session')
def test_app(request):
    """Instantiate a turing tweet app for testing."""
    from webtest import TestApp
    from pyramid.config import Configurator

    def main(global_config, **settings):
        """Return a Pyramid WSGI application."""
        settings['sqlalchemy.url'] = os.environ.get('DATABASE_URL_TESTING')
        config = Configurator(settings=settings)
        config.include('pyramid_jinja2')
        config.include('.models')
        config.include('.routes')
        config.scan()
        return config.make_wsgi_app()

    app = main({})
    testapp = TestApp(app)

    session_factory = app.registry["dbsession_factory"]
    engine = session_factory().bind
    Base.metadata.create_all(bind=engine)

    def tearDown():
        Base.metadata.drop_all(bind=engine)
    request.addfinalizer(tearDown)
    return testapp


@pytest.fixture
def home_response():
    """Return a response from home page."""
    from turingtweets.views.default import home_view
    request = testing.DummyRequest()
    response = home_view(request)
    return response

    # ============Test of POST request===============


@pytest.fixture
def post_request(dummy_request):
    dummy_request.method = "POST"
    return dummy_request


def test_create_post_request(post_request):
    from turingtweets.views.default import home_view
    data = {'fakeTweet': 'I would rather run against Crooked Hillary Clinton, I am running for president and law prohibits. LOVE!'}
    post_request.POST = data
    response = home_view(post_request)
    import pdb; pdb.set_trace()
    assert response == {}

    # ============Tests for Home view routes===============

def test_home_route_returns_response_is_dict(dummy_request):
    """Home view returns a Response Object is dict."""
    from turingtweets.views.default import home_view
    response = home_view(dummy_request)
    assert isinstance(response, dict)


def test_home_view_is_good_dict_has_property(dummy_request):
    """Home view response dict has property."""
    from turingtweets.views.default import home_view
    response = home_view(dummy_request)
    assert response['page'] == 'Home'


def test_home_view_returns_200(testapp_route):
    """Home view response has 200."""
    response = testapp_route.get('/', status=200)
    assert response.status_code == 200


def test_home_view_returns_404(testapp_route):
    """Home view bad request response has 404."""
    response = testapp_route.get('/poop', status=404)
    assert response.status_code == 404


def test_p_tags_are_populated(testapp_route):
    """<p> populated with actual text."""
    response = testapp_route.get('/', status=200)
    html = response.html
    assert html.getText('p') is not None


# # ============Tests for About view routes===============


def test_about_view_returns_200(testapp_route):
    """About view response has 200."""
    response = testapp_route.get('/about', status=200)
    assert response.status_code == 200


def test_about_view_returns_404(testapp_route):
    """About view bad request response has 404."""
    response = testapp_route.get('/about/poop', status=404)
    assert response.status_code == 404


def test_img_tags_are_populated(testapp_route):
    """<img> populated with 4 photos."""
    response = testapp_route.get('/about', status=200)
    html = response.html
    assert len(html.findAll('img')) == 4


def test_p_tags_are_populated(testapp_route):
    """<p> populated on about."""
    response = testapp_route.get('/about', status=200)
    html = response.html
    assert len(html.findAll('p')) == 8

# # ============Tests for Documentation view routes===============


def test_doc_view_returns_200(testapp_route):
    """About view response has 200."""
    response = testapp_route.get('/doc', status=200)
    assert response.status_code == 200


def test_doc_view_returns_404(testapp_route):
    """About view bad request response has 404."""
    response = testapp_route.get('/doc/poop', status=404)
    assert response.status_code == 404


def test_h3_tags_are_populated(testapp_route):
    """<img> populated with 4 photos."""
    response = testapp_route.get('/doc', status=200)
    html = response.html
    assert len(html.findAll('h3')) == 4


def test_h1_tags_are_populated(testapp_route):
    """<h1> populated is on page."""
    response = testapp_route.get('/doc', status=200)
    html = response.html
    assert 'Documentation' in html.text


def test_doc_view_is_good_content(dummy_request):
    """Doc view response dict has property."""
    from turingtweets.views.default import doc_view
    response = doc_view(dummy_request)
    assert response['page'] == 'Documentation'


def test_about_view_is_good_content(dummy_request):
    """About view response dict has property."""
    from turingtweets.views.default import about_view
    response = about_view(dummy_request)
    assert response['page'] == 'About the Team'

# # ============Tests for Real JSON route===============


def test_real_json_returns_200(testapp_route):
    """Real JSON route response has 200."""
    response = testapp_route.get('/real', status=200)
    assert response.status_code == 200


def test_real_json_is_populated(testapp_route):
    """Real JSON route has key of 'tweet'."""
    response = testapp_route.get('/real', status=200)
    assert response.json['tweet'] is not ''


def test_real_json_is_real_tweet(testapp_route):
    """Real JSON response is a real tweet."""
    response = testapp_route.get('/real', status=200)
    HERE = os.path.dirname(__file__)
    with open(os.path.join(HERE, 'models/realdonaldtrump_short.json'), 'r', encoding='utf-8') as json_file:
        json_data = json.load(json_file)
    tweet_list = []
    for tweet in json_data:
        tweet_list.append(tweet['text'])
    assert response.json['tweet'] in tweet_list


# # ============Tests for Fake JSON route===============


def test_fake_json_returns_200(testapp_route):
    """Fake JSON route response has 200."""
    response = testapp_route.get('/fake', status=200)
    assert response.status_code == 200


def test_fake_json_is_populated(testapp_route):
    """Fake JSON route has key of 'tweet'."""
    response = testapp_route.get('/real', status=200)
    assert response.json['tweet'] is not ''


# # ============Tests for Validated Fake JSON route===============


def test_fake_val_json_returns_200(testapp_route):
    """Validated fake JSON route response has 200."""
    response = testapp_route.get('/fake-validated', status=200)
    assert response.status_code == 200


def test_fake_val_json_is_populated(testapp_route):
    """Validated fake JSON route has key of 'tweet'."""
    response = testapp_route.get('/fake-validated', status=200)
    assert response.json['tweet'] is not ''


def test_fake_val_json_is_in_fake_db(testapp_route):
    """Validated fake JSON response is a fake tweet in the DB."""
    response = testapp_route.get('/fake-validated', status=200)
    access_dict = {'sqlalchemy.url': os.environ.get('DATABASE_URL')}
    engine = get_engine(access_dict)
    session_factory = sessionmaker(bind=engine)
    session = session_factory()
    fake_tweets = session.query(FakeTweet).all()
    tweet_list = []
    for tweet in fake_tweets:
        tweet_list.append(tweet.faketweet)
    assert response.json['tweet'] in tweet_list
