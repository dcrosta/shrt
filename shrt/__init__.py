__all__ = ['app']

import flask
app = flask.Flask('shrt')

from os.path import abspath, dirname, exists, join
here = dirname(__file__)
parent = abspath(join(dirname(__file__), '..'))

config = join(parent, 'shrt.cfg')
if exists(config):
    app.config.from_pyfile(config)

private = join(parent, 'private.shrt.cfg')
if exists(private):
    app.config.from_pyfile(private)

from flask.ext.pymongo import PyMongo
mongo = PyMongo(app)

import shrt.views
import shrt.db

@app.before_first_request
def db_setup():
    if not mongo.db.shortened.last.find_one():
        mongo.db.shortened.last.save({'_id': 'last', 'last': 0})

    mongo.db.shortened.ensure_index('url')

