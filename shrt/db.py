import pymongo

from flask import g

from shrt import app

conn = None
db = None

def setup(hostname, username, password, database, port):
    global conn
    global db

    port = int(port)

    conn = pymongo.Connection(host=hostname, port=port)
    db = conn[database]
    if username and password:
        db.authenticate(username, password)

    if not db.shortened.last.find_one():
        db.shortened.last.save({'_id': 'last', 'last': 0})

    db.shortened.ensure_index('url')

@app.before_request
def add_db_to_g():
    global db
    g.db = db

