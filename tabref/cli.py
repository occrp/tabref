import click
import logging
from pprint import pprint  # noqa

from tabref.matcher import create_matcher
from tabref.csv import CsvTableSearcher
from tabref.sql import SqlTableSearcher, connect_db

log = logging.getLogger('tabref')


@click.group()
@click.option('--debug/--no-debug', default=False)
@click.pass_context
def cli(ctx, debug):
    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(level=level)
    logging.getLogger('requests').setLevel(logging.WARNING)
    ctx.obj['debug'] = debug


@cli.command()
@click.pass_context
@click.option('db', '--db', envvar='DATABASE_URI', required=True)
@click.option('tables', '--table', '-t', multiple=True)
@click.option('out_path', '--out-path', '-o', default='results')
@click.option('match_list', '--match-list', '-m', required=True)
def sql(ctx, db, tables, out_path, match_list):
    meta = connect_db(db)
    matcher = create_matcher(match_list)
    if not len(tables):
        tables = meta.tables
    for table in tables:
        searcher = SqlTableSearcher(matcher, out_path, meta, table)
        searcher.process()


@cli.command()
@click.pass_context
@click.option('out_path', '--out-path', '-o', default='results')
@click.option('match_list', '--match-list', '-m', required=True)
@click.argument('path')
def csv(ctx, path, out_path, match_list):
    matcher = create_matcher(match_list)
    searcher = CsvTableSearcher(matcher, out_path, path)
    searcher.process()


def main():
    cli(obj={})


if __name__ == '__main__':
    main()
