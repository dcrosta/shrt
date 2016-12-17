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

from flask_sqlalchemy import SQLAlchemy
sqla = SQLAlchemy(app)

# load the views module
from shrt import views
