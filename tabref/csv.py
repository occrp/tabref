import logging
from normality import slugify, guess_encoding
from unicodecsv import DictReader

from tabref.searcher import TableSearcher

log = logging.getLogger(__name__)


class CsvTableSearcher(TableSearcher):

    def __init__(self, matcher, out_dir, file_name):
        self.file_name = file_name
        base_name = slugify(file_name, sep='_')
        super(CsvTableSearcher, self).__init__(matcher, out_dir, base_name)

    def rows(self):
        try:
            with open(self.file_name, 'r') as fh:
                encoding = guess_encoding(fh.read(4096 * 10))
                fh.seek(0)
                for row in DictReader(fh, encoding=encoding):
                    yield row
        except Exception as exc:
            log.error('Failed reading file [%s]: %s', self.file_name, exc)
