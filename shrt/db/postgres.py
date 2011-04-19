import psycopg2.pool

from shrt.db import shortstr

pool = None

def setup(**kwargs):
    global pool

    kwargs = dict((k, v) for k, v in kwargs.iteritems() if v is not None)

    hostname = kwargs.pop('hostname', 'localhost')
    username = kwargs.pop('username', None)
    password = kwargs.pop('password', None)
    database = kwargs.pop('database', 'shrt')
    port = int(kwargs.pop('port', 5432))

    pool_min = int(kwargs.pop('pool_min', 1))
    pool_max = int(kwargs.pop('pool_min', 3))

    pool_kwargs = dict(
        host=hostname,
        port=port,
        user=username,
        password=password,
        database=database)
    pool_kwargs = dict((k, v) for k, v in pool_kwargs.items() if v is not None)

    pool = psycopg2.pool.ThreadedConnectionPool(pool_min, pool_max, **pool_kwargs)

    try:
        conn = pool.getconn()
        curs = conn.cursor()
        curs.execute('select version from schema_info')

    except:
        # first, undo the aborted transaction
        conn.rollback()

        # set up schema
        curs = conn.cursor()
        curs.execute("create table url (short varchar(256) not null, long varchar(65535) not null, unique(short), unique(long))")
        curs.execute("create sequence url_seq start with 1")
        curs.execute("create table schema_info (version integer not null)")
        curs.execute("insert into schema_info (version) values (1)")
        conn.commit()

    finally:
        curs.close()
        pool.putconn(conn)

def new_url(long):
    try:
        conn = pool.getconn()
        curs = conn.cursor()

        curs.execute("select nextval('url_seq')")
        nextid = curs.fetchone()[0]
        short = shortstr(nextid)

        curs.execute("insert into url (short, long) values (%s, %s)", (short, long))
        conn.commit()
    finally:
        curs.close()
        pool.putconn(conn)

    return (short, long)

def get_url(short=None, long=None):
    if short:
        query = "select short, long from url where short = %s"
        args = (short, )
    elif long:
        query = "select short, long from url where long = %s"
        args = (long, )
    else:
        return (None, None)

    try:
        conn = pool.getconn()
        curs = conn.cursor()

        curs.execute(query, args)
        short, long= curs.fetchone()

        return (short, long)

    except:
        # not found
        conn.rollback()

    finally:
        curs.close()
        pool.putconn(conn)

    return (None, None)

