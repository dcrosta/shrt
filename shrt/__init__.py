__all__ = ['app']

import flask
app = flask.Flask('shrt')

import shrt.views
import shrt.db

def niceify(settings):
    for key, value in settings.items():
        if value.lower() == 'true':
            value = True
        elif value.lower() == 'false':
            value = False
        if key.endswith('_dir') or key.endswith('_path'):
            value = abspath(value)
        settings[key] = value
    return settings

def app_factory(global_config, **settings):
    settings = niceify(settings)
    app.debug = settings.pop('debug', False)

    shrt.db.setup(
        hostname=settings.pop('mongo_hostname', 'localhost'),
        username=settings.pop('mongo_username', ''),
        password=settings.pop('mongo_password', ''),
        database=settings.pop('mongo_database', 'shrt'),
        port=settings.pop('mongo_port', 27017),
    )

    return app

