def includeme(config):
    config.add_static_view('static', 'turingtweets:static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('about', '/about')
    config.add_route('documentation', '/doc')
    config.add_route('json-fake', '/fake')
    config.add_route('json-fake-validated', '/fake-validated')
    config.add_route('json-real', '/real')
