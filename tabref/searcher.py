import os
import logging
from unicodecsv import writer
from collections import OrderedDict

from tabref.util import normalize_value

log = logging.getLogger(__name__)


class TableSearcher(object):

    def __init__(self, matcher, out_dir, base_name):
        self.matcher = matcher
        self.out_dir = out_dir
        self.base_name = base_name
        try:
            os.makedirs(self.out_dir)
        except:
            pass
        self.result_writer = None

    def write_result(self, result):
        if self.result_writer is None:
            self.headers = result.keys()
            result_path = '%s.csv' % self.base_name
            result_path = os.path.join(self.out_dir, result_path)
            self.result_fh = open(result_path, 'w')
            self.result_writer = writer(self.result_fh)
            self.result_writer.writerow(self.headers)
        self.result_writer.writerow([result.get(h) for h in self.headers])

    def match_row(self, row):
        matches = False
        for key, text in row.items():
            # see if this the cell value clearly numeric:
            try:
                float(text)
                continue
            except:
                pass
            norm = normalize_value(text)
            if norm is None:
                continue
            for (_, match) in self.matcher.iter(norm):
                result = OrderedDict(row.items())
                result['_match_name'] = match
                result['_match_field'] = key
                self.write_result(result)
                matches = True
        return matches

    def process(self):
        matches = 0
        for count, row in enumerate(self.rows()):
            if self.match_row(row):
                matches += 1

            if count % 10000 == 0 and count > 0:
                log.info("[%s] done: %s rows, %s matches",
                         self.base_name, count, matches)

        if self.result_writer is not None:
            self.result_fh.close()
