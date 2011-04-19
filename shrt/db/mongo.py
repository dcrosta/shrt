import pymongo

from shrt.db import shortstr

conn = None
mdb = None

def setup(**kwargs):
    global conn
    global mdb

    kwargs = dict((k, v) for k, v in kwargs.iteritems() if v is not None)

    hostname = kwargs.pop('hostname', 'localhost')
    username = kwargs.pop('username', None)
    password = kwargs.pop('password', None)
    database = kwargs.pop('database', 'shrt')
    port = int(kwargs.pop('port', 27017))

    conn = pymongo.Connection(host=hostname, port=port)
    mdb = conn[database]
    if username and password:
        mdb.authenticate(username, password)

    if not mdb.shortened.last.find_one():
        mdb.shortened.last.save({'_id': 'last', 'last': 0})

    mdb.shortened.ensure_index('url')

def new_url(long):
    nextid = mdb.command('findAndModify', 'shortened.last', update={'$inc': {'last': 1}}, new=True)
    nextid = int(nextid['value']['last'])

    short= shortstr(nextid)
    mdb.shortened.save({'_id': short, 'url': long})

    return (short, long)

def get_url(short=None, long=None):
    if short:
        query = {'_id': short}
    elif long:
        query = {'url': long}

    doc = mdb.shortened.find_one(query)
    if not doc:
        return (None, None)
    return (doc['_id'], doc['url'])
