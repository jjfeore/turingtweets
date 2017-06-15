"""
Tests for turing tweets
"""
import pytest
import os
from pyramid import testing
from pyramid.response import Response
from turingtweets.models.mymodel import Tweet
from pyramid.httpexceptions import HTTPNotFound
from turingtweets.models.meta import Base

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
    SessionFactory = configuration.registry["dbsession_factory"]
    session = SessionFactory()
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
    """Creates a dummy post request."""
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
    from webtest import TestApp
    from pyramid.config import Configurator

    def main(global_config, **settings):
        """ This function returns a Pyramid WSGI application.
        """
        settings['sqlalchemy.url'] = os.environ.get('DATABASE_URL_TESTING')
        config = Configurator(settings=settings)
        config.include('pyramid_jinja2')
        config.include('.models')
        config.include('.routes')
        config.scan()
        return config.make_wsgi_app()

    app = main({})
    testapp = TestApp(app)

    SessionFactory = app.registry["dbsession_factory"]
    engine = SessionFactory().bind
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
    import pdb; pdb.set_trace()
    assert len(html.findAll('img')) == 4
