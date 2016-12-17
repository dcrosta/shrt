from shrt import sqla

__all__ = ('new_url', 'get_url', 'setup', 'shortstr')


class Shortened(sqla.Model):
    id = sqla.Column(sqla.Integer, primary_key=True)
    fragment = sqla.Column(sqla.String(32), nullable=False, unique=True)
    url = sqla.Column(sqla.String(2048), nullable=False, unique=True)

    @classmethod
    def find(cls, short=None, long=None):
        if long and not short:
            return cls.query.filter(cls.url == long).first()
        elif short and not long:
            return cls.query.filter(cls.fragment == short).first()
        else:
            raise ValueError("set either short or long")

    @classmethod
    def new(cls, url):
        conn = sqla.engine.connect()
        try:
            result = conn.execute("select nextval('shortened_id_seq'::regclass)")
            next_id, = next(iter(result))
        finally:
            conn.close()

        instance = cls(
            id=next_id,
            fragment=shortstr(next_id),
            url=url,
        )
        sqla.session.add(instance)
        sqla.session.commit()
        return instance


def new_url(long):
    new = Shortened.new(long)
    return (new.fragment, new.url)

def get_url(short=None, long=None):
    found = Shortened.find(short, long)
    if not found:
        return (None, None)
    return (found.fragment, found.url)

digit='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
count=len(digit)
def shortstr(num):
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

def inv_shortstr(short):
    """
    >>> inv_shortstr('a')
    1
    >>> inv_shortstr('b')
    2
    >>> inv_shortstr('9')
    62
    >>> inv_shortstr('aa')
    63
    >>> inv_shortstr('ab')
    64
    >>> inv_shortstr('hdrg')
    1923123
    """
    out = 0
    for letter in short:
        out *= len(digit)
        out += digit.index(letter) + 1
    return out


if __name__ == '__main__':
    import doctest
    doctest.testmod()
