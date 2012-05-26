from shrt import mongo

__all__ = ('new_url', 'get_url', 'setup', 'shortstr')

def new_url(long):
    nextid = mongo.db.shortened.last.find_and_modify(
        {'_id': 'last'}, {'$inc': {'last': 1}}, new=True)
    nextid = int(nextid['last'])

    short = shortstr(nextid)
    mongo.db.shortened.save({'_id': short, 'url': long})

    return (short, long)

def get_url(short=None, long=None):
    if short:
        query = {'_id': short}
    elif long:
        query = {'url': long}

    doc = mongo.db.shortened.find_one(query)
    if not doc:
        return (None, None)
    return (doc['_id'], doc['url'])

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

if __name__ == '__main__':
    import doctest
    doctest.testmod()

