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

    db_type = settings.pop('db_type')
    print "using", db_type

    db_kwargs = {}
    for key in settings.keys():
        if key.startswith(db_type):
            value = settings.pop(key)
            key = key[len(db_type)+1:]
            db_kwargs[key] = value
    shrt.db.setup(db_type=db_type, **db_kwargs)

    return app

