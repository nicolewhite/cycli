# cycli
A Command Line Interface for Neo4j's Cypher Query Language.

![demo](screenshots/output.gif)

## Install

### Stable Release from PyPI

```
$ pip install cycli
```

### Latest Development Release

```
$ git clone https://github.com/nicolewhite/cycli.git
$ sudo python cycli/setup.py install
```

## Start

To start, simply execute `cycli` from your terminal.

```
$ cycli
```

If you have Neo4j authentication enabled, you'll need to pass a username.

```
$ cycli -u username
```

You will then be prompted to enter your password. For more options, execute `cycli --help`.

## Features

### Autocomplete

The smart autocompletion suggests node labels when you're drawing a node, relationship types when you're drawing
a relationship, and properties when working with identifiers. Of course, it also suggests all of the Cypher keywords,
functions, and predicates.

#### Node Labels

![labels](screenshots/autocomplete-labels.png)

#### Relationship Types

![rels](screenshots/autocomplete-rels.png)

#### Properties

![props](screenshots/autocomplete-props.png)

#### Cypher Keywords

![cypher](screenshots/autocomplete-cypher.png)

### Syntax Highlighting

Catch syntax errors with the built-in syntax highlighting. The colors were chosen to emulate the syntax highlighting
available in the Neo4j browser.

![syntax](screenshots/syntax-highlight.png)

## Usage

### Execute Queries

Execute queries by ending them with a semicolon and pressing enter or by pressing enter twice.

### Abort Queries

While a query is executing, CTRL-C will abort the query and rollback the transaction.

### Get Help

Type "help" to see a table of keywords / keystrokes and their descriptions.

![help](screenshots/help.png)

### Exiting

Exit cycli by typing "quit" or "exit" or by pressing CTRL-D on an empty line.

## Credits

This project depends heavily on [python-prompt-toolkit](https://github.com/jonathanslenders/python-prompt-toolkit) and
[py2neo](https://github.com/nigelsmall/py2neo).