import os
import logging
from unicodecsv import writer
from collections import OrderedDict
from collections import defaultdict
from Queue import Queue
from threading import RLock, Thread
from pprint import pprint  # noqa
import multiprocessing

from tabref.util import normalize_value, decode_path

log = logging.getLogger(__name__)


class TableSearcher(object):

    def __init__(self, matcher, out_dir, base_name):
        self.matcher = matcher
        self.out_dir = decode_path(out_dir)
        self.base_name = base_name
        self.queue = Queue(maxsize=50000)
        self.match_count = 0
        self.lock = RLock()
        try:
            os.makedirs(self.out_dir)
        except:
            pass
        self.result_writer = None

    def write_result(self, result):
        self.lock.acquire()
        try:
            if self.result_writer is None:
                self.headers = result.keys()
                result_path = '%s.csv' % self.base_name
                result_path = decode_path(result_path)
                result_path = os.path.join(self.out_dir, result_path)
                self.result_fh = open(result_path, 'w')
                self.result_writer = writer(self.result_fh)
                self.result_writer.writerow(self.headers)
            self.result_writer.writerow([result.get(h) for h in self.headers])
        finally:
            self.lock.release()

    def finalize(self):
        self.lock.acquire()
        try:
            if self.result_writer is not None:
                self.result_fh.close()
        finally:
            self.lock.release()

    def match_row(self, row):
        matches = defaultdict(list)

        for key, text in row.items():
            norm = normalize_value(text)
            if norm is None:
                continue

            for (_, match) in self.matcher.iter(norm):
                matches[match].append(key)

        for match, fields in matches.items():
            result = OrderedDict(row.items())
            result['_match_name'] = match
            result['_match_field'] = ', '.join(fields)
            # pprint(dict(result))
            self.write_result(result)
            self.match_count += 1

    def handle_row(self):
        while True:
            item = self.queue.get()
            self.match_row(item)
            self.queue.task_done()

    def process(self):
        num_threads = multiprocessing.cpu_count()
        log.info("Process [%s threads]: %s", num_threads, self.base_name)
        for i in range(num_threads):
            thread = Thread(target=self.handle_row)
            thread.daemon = True
            thread.start()

        for count, row in enumerate(self.rows()):
            self.queue.put(row)
            # self.match_row(row)

            if count % 10000 == 0 and count > 0:
                log.info("[%s] done: %s rows, %s matches, %d queued",
                         self.base_name, count, self.match_count,
                         self.queue.qsize())

        self.queue.join()
        self.finalize()
