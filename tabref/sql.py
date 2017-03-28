from sqlalchemy import create_engine, MetaData, Table

from tabref.searcher import TableSearcher


def connect_db(uri):
    db = create_engine(uri)
    meta = MetaData(bind=db)
    meta.reflect(bind=db)
    return meta


class SqlTableSearcher(TableSearcher):

    def __init__(self, matcher, out_dir, db, table):
        self.meta = db
        self.table = Table(table, self.meta, autoload=True)
        super(SqlTableSearcher, self).__init__(matcher, out_dir, table)

    def rows(self):
        rp = self.meta.bind.execute(self.table.select())
        while True:
            rows = rp.fetchmany(10000)
            if rows is None or not len(rows):
                break
            for row in rows:
                yield row
