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
            rows = rp.fetchmany(100000)
            if rows is None or not len(rows):
                break
            for row in rows:
                yield row

    @classmethod
    def connect_db(cls, uri):
        db = create_engine(uri)
        meta = MetaData(bind=db)
        meta.reflect(bind=db)
        return meta


def match_db(matcher, out_dir, uri, prefix=None):
    meta = SqlTableSearcher.connect_db(uri)
    for table in meta.tables:
        if prefix is not None and not table.startswith(prefix):
            continue
        grep = SqlTableSearcher(matcher, out_dir, uri, table)
        grep.process()
