import logging
from normality import slugify, guess_encoding
from unicodecsv import DictReader, Sniffer

from tabref.searcher import TableSearcher
from tabref.util import decode_path

log = logging.getLogger(__name__)


class CsvTableSearcher(TableSearcher):

    def __init__(self, matcher, out_dir, file_name):
        self.file_name = decode_path(file_name)
        base_name = slugify(file_name, sep='_')
        super(CsvTableSearcher, self).__init__(matcher, out_dir, base_name)

    def rows(self):
        try:
            with open(self.file_name, 'r') as fh:
                sample = fh.read(4096 * 10)
                encoding = guess_encoding(sample)
                if encoding != 'utf-8':
                    log.info("Decode [%s]: %s", self.file_name, encoding)
                sample = sample.decode(encoding, 'replace')
                dialect = Sniffer().sniff(sample)
                fh.seek(0)
                for row in DictReader(fh, encoding=encoding, delimiter=dialect.delimiter.encode(encoding)):
                    yield row
        except Exception as exc:
            log.error('Failed reading file [%s]: %s', self.file_name, exc)
