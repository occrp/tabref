import logging
from unicodecsv import DictReader
from ahocorasick import Automaton

from tabref.util import normalize_value, decode_path

log = logging.getLogger(__name__)


def is_superset(token, tokens):
    """If a token is a superset of another one, don't include it."""
    for other in tokens:
        if other == token:
            continue
        if other in token:
            return True
    return False


def create_matcher(file_name):
    tokens = {}
    with open(decode_path(file_name), 'r') as fh:
        for row in DictReader(fh):
            name = row.get('name')
            token = normalize_value(name)
            if token is None:
                continue
            tokens[token] = name.strip()

    automaton = Automaton()
    token_count = 0
    for token, name in tokens.items():
        if is_superset(token, tokens.keys()):
            continue
        automaton.add_word(token, name)
        token_count += 1
    automaton.make_automaton()
    log.info("Generated %d search terms from: %s",
             token_count, file_name)
    return automaton
