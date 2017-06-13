def includeme(config):
    config.add_static_view('static', 'turingteets:static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('about', '/about')
    config.add_route('about', '/about')
