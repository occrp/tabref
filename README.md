# tabref

``tabref`` is a tool for cross-referencing datasets with a (potentially large)
list of search terms. For example, it could be used to search mentions of a set
of company or person names in a large stash of CSV files, or within tables in
a database.

Here's why it's useful:

* The tool will search across large amounts of data reasonably quickly and
  simply.
* It's optimized to search people and company mentions, using text
  and company name normalization to produce matches more flexibly.

## Usage

Here's what you need to get started with ``tabref``:

* A CSV file with a "name" column to be used as a set of search terms.
* Either a CSV file, a directory of CSV files, or a database connection URI
  that contains tables you want to search across.

After running, ``tabref`` will drop a CSV file into the specified output
directory that contains all the matching rows in the source CSV file or SQL
table. The output file will also contain extra ``_match`` columns that describe
the matching search term and match location.

```bash
# Search all tables in `mydb`:
$ tabref sql --db postgresql://localhost/mydb --match-list searches.csv --out-path matches/

# Search only the table `mytable`:
$ tabref sql --db postgresql://localhost/mydb --match-list searches.csv --out-path matches/ --table mytable

# Search inside a CSV file:
$ tabref csv --match-list searches.csv --out-path matches/ mycsv.csv
```
