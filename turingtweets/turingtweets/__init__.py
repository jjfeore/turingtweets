from pyramid.config import Configurator
import os


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application."""
    if os.environ.get('HEROKU_POSTGRESQL_COBALT_URL', ''):
        settings["sqlalchemy.url"] = os.environ["HEROKU_POSTGRESQL_COBALT_URL"]
    config = Configurator(settings=settings)
    config.include('pyramid_jinja2')
    config.include('.models')
    config.include('.routes')
    config.scan()
    return config.make_wsgi_app()
