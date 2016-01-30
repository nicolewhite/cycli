# cycli [![Build Status](https://travis-ci.org/nicolewhite/cycli.svg?branch=master)](https://travis-ci.org/nicolewhite/cycli) [![PyPi version](https://badge.fury.io/py/cycli.svg)](https://pypi.python.org/pypi/cycli/)

A command-line interface for [Neo4j](http://neo4j.com/)'s graph query language, Cypher.

<p align="center">
  <img src="screenshots/output.gif" />
</p>

## Install

If you haven't already, [download](http://neo4j.com/download/other-releases/) and install Neo4j. Then, install `cycli`:

```
$ pip install cycli
```

## Start

To start, simply execute `cycli` from your terminal. Neo4j needs to be running.

```
$ cycli
```

If you have Neo4j authentication enabled, you'll need to pass a username.

```
$ cycli -u username
```

You will then be prompted to enter your password. For more options, execute `cycli --help`.

```
$ cycli --help
Usage: cycli [OPTIONS]

Options:
  -v, --version            Show cycli version and exit.
  -h, --host TEXT          The host address of Neo4j.
  -P, --port TEXT          The port number on which Neo4j is listening.
  -u, --username TEXT      Username for Neo4j authentication.
  -p, --password TEXT      Password for Neo4j authentication.
  -t, --timeout INTEGER    Set a global socket timeout for queries.
  -l, --logfile FILENAME   Log every query and its results to a file.
  -f, --filename FILENAME  Execute semicolon-separated Cypher queries from a
                           file.
  -s, --ssl                Use the HTTPS protocol.
  -r, --read-only          Do not allow any write queries.
  --help                   Show this message and exit.
```

## Autocomplete

The smart autocompletion suggests node labels when you're drawing a node, relationship types when you're drawing
a relationship, and properties when working with identifiers. Of course, it also suggests all of the Cypher keywords,
functions, and predicates.

### Node Labels

![labels](screenshots/autocomplete-labels.png)

### Relationship Types

![rels](screenshots/autocomplete-rels.png)

### Properties

![props](screenshots/autocomplete-props.png)

### Cypher Keywords

Cypher keywords are displayed in a [probabilistic order based on your most recent keyword](http://nicolewhite.github.io/2015/10/05/improving-cycli-autocomplete-markov-chains.html).

![cypher](screenshots/autocomplete-cypher.png)

### Opening Characters

If you type `(`, `[`, `{`, `"`, or `'`, a matching closing character is automatically placed to the right of your cursor.

![matching](screenshots/autocomplete-matching.png)

## Syntax Highlighting

Catch syntax errors with the built-in syntax highlighting. The colors were chosen to emulate the syntax highlighting
available in the Neo4j browser.

![syntax](screenshots/syntax-highlight.png)

## Usage

### Execute Queries

Execute queries by ending them with a semicolon and pressing enter or by pressing enter twice.

### Keywords

Type "help" to see a table of keywords / keystrokes and their descriptions.

Keyword            | Description
-------------------|--------------------------------------------------------------
quit               | Exit cycli.
exit               | Exit cycli.
help               | Display this text.
refresh            | Refresh schema cache.
run-n              | Run a Cypher query n times.
export             | Set a parameter with export key=value.
schema             | Display indexes, constraints, labels, and relationship types.
schema-indexes     | Display indexes.
schema-constraints | Display constraints.
schema-labels      | Display labels.
schema-rels        | Display relationship types.
CTRL-D             | Exit cycli if the input is blank.
CTRL-C             | Abort and rollback the currently-running query.

### `run-n`

Run a Cypher query `n` times. This is useful for large updates, e.g. if you want to update a property in batches.

```
> MATCH (n) RETURN COUNT(*);
   | COUNT(*)
---+----------
 1 |      456

26 ms
```

Let's say we want to add a new property in batches of 100. If we have 456 nodes, we'll need to run the same Cypher query
5 times.

```
> run-5 MATCH (n)
WHERE NOT HAS(n.newProperty)
WITH n LIMIT 100
SET n.newProperty = "Hello World"
RETURN COUNT(*);
   | COUNT(*)
---+----------
 1 |      100

Run 1: 44 ms

   | COUNT(*)
---+----------
 1 |      100

Run 2: 8 ms

   | COUNT(*)
---+----------
 1 |      100

Run 3: 8 ms

   | COUNT(*)
---+----------
 1 |      100

Run 4: 10 ms

   | COUNT(*)
---+----------
 1 |       56

Run 5: 9 ms

Total duration: 79 ms
```

### `export`

Set parameters with `export key=value`.

```
> export name="Tom Hanks"
> export year=2005
> env
name=Tom Hanks
year=2005
> MATCH (p:Person {name:{name}})-[:ACTED_IN]->(m:Movie)
WHERE m.released > {year}
RETURN m.title, m.released;
   | m.title              | m.released
---+----------------------+------------
 1 | Charlie Wilson's War |       2007
 2 | Cloud Atlas          |       2012
 3 | The Da Vinci Code    |       2006

12 ms
```

The `value` is evaluated with Python's `eval`, so you can also do things like this:

```
> export evens=[x for x in range(10) if x % 2 == 0]
> env["evens"]
[0, 2, 4, 6, 8]
```

## Using `cycli` with Bolt

[Bolt](http://neo4j.com/blog/neo4j-3-0-milestone-1-release/) is Neo4j's new binary protocol. It is still in the
pre-release stage and `cycli`'s support of Bolt should be considered an alpha feature. You can use Bolt with `cycli` by
installing [Neo4j 3.0](http://alpha.neohq.net/), disabling authentication, and following the below steps:

```
$ pip install virtualenv
$ virtualenv cycli-bolt
$ source cycli-bolt/bin/activate
$ pip install cycli
$ git clone https://github.com/neo4j/neo4j-python-driver.git
$ python neo4j-python-driver/setup.py install
$ cycli
```

## Credits

This project depends heavily on [python-prompt-toolkit](https://github.com/jonathanslenders/python-prompt-toolkit) and
[py2neo](https://github.com/nigelsmall/py2neo). I also frequently reference the [pgcli](https://github.com/dbcli/pgcli)
and [mycli](https://github.com/dbcli/mycli) projects for ideas and troubleshooting help. The logo was designed by Greta Workman. =)

<p align="center">
  <img src="screenshots/logo.png" />
</p>
