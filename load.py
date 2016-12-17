from shrt import sqla
from shrt import db


sqla.drop_all()
sqla.create_all()

session = sqla.session()
for line in open("data.txt"):
    line = line.strip().split("\t")
    id = int(line[0])
    fragment = line[1]
    url = line[2]

    row = db.Shortened(
        id=id,
        fragment=fragment,
        url=url,
    )
    session.add(row)

session.commit()

conn = sqla.engine.connect()

result = conn.execute('select max(id) from shortened')
max_id, = next(iter(result))

conn.execute('alter sequence shortened_id_seq restart with %d' % (max_id + 1))
