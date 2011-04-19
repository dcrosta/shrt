__all__ = ['new_url', 'get_url', 'setup', 'shortstr']

_new_url = None
_get_url = None

def setup(db_type, **kwargs):
    global _new_url
    global _get_url

    if db_type == 'mongo':
        import shrt.db.mongo
        shrt.db.mongo.setup(**kwargs)
        _new_url = shrt.db.mongo.new_url
        _get_url = shrt.db.mongo.get_url

    elif db_type == 'postgres':
        import shrt.db.postgres
        shrt.db.postgres.setup(**kwargs)
        _new_url = shrt.db.postgres.new_url
        _get_url = shrt.db.postgres.get_url

    else:
        raise ValueError('unknown db_type: %s' % db_type)

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

def new_url(long):
    # create a new shortened url, and return
    # (short, long) as stored in the db
    #
    # implementations of this function may
    # assume that the long url does not yet
    # exist in the persistent store
    return _new_url(long)

def get_url(short=None, long=None):
    # find an existing short url by either
    # short or long; return (None, None)
    # if no such short url exists
    return _get_url(short=short, long=long)

if __name__ == '__main__':
    import doctest
    doctest.testmod()

