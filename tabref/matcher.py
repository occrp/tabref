import logging
from unicodecsv import DictReader
from ahocorasick import Automaton

from tabref.util import normalize_value

log = logging.getLogger(__name__)


def create_matcher(file_name):
    automaton = Automaton()
    token_count = 0
    with open(file_name, 'r') as fh:
        for row in DictReader(fh):
            name = row.get('name')
            token = normalize_value(name)
            # TODO: do cool name permutations
            if token is None:
                continue
            automaton.add_word(token, name.strip())
            token_count += 1
    automaton.make_automaton()
    log.info("Generated %d search terms from: %s",
             token_count, file_name)
    return automaton
