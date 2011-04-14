import urllib
import string

import flask
from flask import render_template
from flask import request
from flask import g

from shrt import app

digit='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
count=len(digit)
def shortstr(num, deep=False):
    """
    >>> shortstr(0)
    >>> shortstr(1)
    'a'
    >>> shortstr(2)
    'b'
    >>> shortstr(62)
    '9'
    >>> shortstr(63)
    'aa'
    >>> shortstr(64)
    'ab'
    >>> shortstr(1923123)
    'hdrg'
    """
    if num <= 0:
        return None
    out = []
    while num:
        num, mod = divmod(num-1, count)
        out.append(digit[mod])
    return ''.join(reversed(out))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/n')
def new():
    if 'url' not in request.args:
        flask.abort(400)

    url = request.args['url']
    url = urllib.unquote(url)

    if not (url.startswith('http://') or url.startswith('https://')):
        flask.abort(400)

    existing = g.db.shortened.find_one({'url': url})
    if existing:
        s = existing['_id']
    else:
        # if this fails, we will just 500, which
        # is all we can do anyway. no need to
        # check for success or anything, then
        nextid = g.db.command('findAndModify', 'shortened.last', update={'$inc': {'last': 1}}, new=True)
        nextid = int(nextid['value']['last'])

        s = shortstr(nextid)
        g.db.shortened.save({'_id':s, 'url': url})

    shorturl = flask.url_for('redirect', shortened=s, _external=True)
    return render_template('new.html', shorturl=shorturl)

@app.route('/<shortened>')
def redirect(shortened):
    url = g.db.shortened.find_one({'_id': shortened}, {'url':1})['url']
    return flask.redirect(url, code=301)

if __name__ == '__main__':
    import doctest
    doctest.testmod()

