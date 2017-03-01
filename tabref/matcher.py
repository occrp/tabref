from unicodecsv import DictReader
from ahocorasick import Automaton

from tabref.util import normalize_value


def create_matcher(file_name):
    automaton = Automaton()
    with open(file_name, 'r') as fh:
        for row in DictReader(fh):
            name = row.get('name')
            token = normalize_value(name)
            # TODO: do cool name permutations
            if token is None:
                continue
            automaton.add_word(token, name.strip())
    automaton.make_automaton()
    return automaton
