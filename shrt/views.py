import urllib
import string
from textwrap import dedent

import flask
from flask import render_template
from flask import request
from flask import g

from shrt import app
from shrt import db

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/_new')
def new():
    if 'url' not in request.args:
        flask.abort(400)

    url = request.args['url']
    url = urllib.unquote(url)

    if not (url.startswith('http://') or url.startswith('https://')):
        flask.abort(400)

    short, long = db.get_url(long=url)
    if not short:
        short, long = db.new_url(long=url)

    return render_template('new.html', short=short)

@app.route('/robots.txt')
def robots():
    return dedent("""\
        User-Agent: *
        Disallow: /
        """)

@app.route('/<short>')
def redirect(short):
    short, long = db.get_url(short=short)
    return flask.redirect(long, code=301)

@app.route('/favicon.ico')
@app.route('/robots.txt')
def nothing():
    flask.abort(404)
