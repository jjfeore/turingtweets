from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from turingtweets.models import mymodel

from pyramid.httpexceptions import (
    HTTPNotFound,
    HTTPFound
)


@view_config(route_name='home', renderer='../templates/mytemplate.jinja2')
def home_view(request):
    """View for home route."""
    return {}
