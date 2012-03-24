__all__ = ['app']

import flask
app = flask.Flask('shrt')

from os.path import abspath, dirname, exists, join
here = dirname(__file__)
parent = abspath(join(dirname(__file__), '..'))

config = join(parent, 'plog.cfg')
if exists(config):
    app.config.from_pyfile(config)

private = join(parent, 'private.plog.cfg')
if exists(private):
    app.config.from_pyfile(private)

import shrt.views
import shrt.db

db_kwargs = {}
db_type = app.config.get('DB_TYPE', 'mongo')
for key, value in app.config.iteritems():
    if key.startswith(db_type.upper() + '_'):
        key = key[len(db_type)+1:]
        db_kwargs[key] = value
shrt.db.setup(db_type=db_type, **db_kwargs)
