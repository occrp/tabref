import os
import click
import logging
from pprint import pprint  # noqa

from tabref.matcher import create_matcher
from tabref.csv import CsvTableSearcher
from tabref.sql import SqlTableSearcher, connect_db
from tabref.util import decode_path

log = logging.getLogger('tabref')


@click.group()
@click.option('--debug/--no-debug', default=False, help="Set verbose output")
@click.pass_context
def cli(ctx, debug):
    """Data cross-referencing tool for entity search lists."""
    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(level=level)
    logging.getLogger('requests').setLevel(logging.WARNING)
    ctx.obj['debug'] = debug


@cli.command()
@click.pass_context
@click.option('db', '--db', envvar='DATABASE_URI', required=True,
              help="Database connection string")
@click.option('tables', '--table', '-t', multiple=True,
              help="Table name")
@click.option('out_path', '--out-path', '-o', default='results',
              type=click.Path(), help="Result CSV folder")
@click.option('match_list', '--match-list', '-m', required=True,
              type=click.Path(exists=True),
              help="CSV file with search terms")
def sql(ctx, db, tables, out_path, match_list):
    """Cross-reference a SQL database table against the match list."""
    meta = connect_db(db)
    matcher = create_matcher(match_list)
    if not len(tables):
        tables = meta.tables
    for table in tables:
        searcher = SqlTableSearcher(matcher, out_path, meta, table)
        searcher.process()


@cli.command()
@click.pass_context
@click.option('out_path', '--out-path', '-o', default='results',
              type=click.Path(), help="Result CSV folder")
@click.option('match_list', '--match-list', '-m', required=True,
              type=click.Path(exists=True),
              help="CSV file with search terms")
@click.argument('path')
def csv(ctx, path, out_path, match_list):
    """Cross-reference a CSV, or folder of CSV files against the match list."""
    matcher = create_matcher(match_list)
    path = decode_path(path)
    out_path = decode_path(out_path)

    if not os.path.exists(path):
        log.error("File does not exist: %s", path)
        return

    if not os.path.isdir(path):
        searcher = CsvTableSearcher(matcher, out_path, path)
        searcher.process()
        return

    for (dirpath, dirnames, filenames) in os.walk(path):
        dirpath = os.path.join(path, dirpath)
        for filename in filenames:
            filepath = os.path.join(dirpath, decode_path(filename))
            searcher = CsvTableSearcher(matcher, out_path, filepath)
            searcher.process()


def main():
    cli(obj={})


if __name__ == '__main__':
    main()
