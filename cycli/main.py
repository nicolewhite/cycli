from __future__ import unicode_literals, print_function

import sys
import click
import re

from prompt_toolkit import Application, CommandLineInterface, AbortAction
from prompt_toolkit.history import History
from prompt_toolkit.shortcuts import create_default_layout, create_eventloop
from prompt_toolkit.filters import Always
from pygments.token import Token

from py2neo.error import Unauthorized
from py2neo.packages.httpstream import SocketError, http

from cycli import __version__
from cycli.lexer import CypherLexer
from cycli.style import CypherStyle
from cycli.completer import CypherCompleter
from cycli.buffer import CypherBuffer
from cycli.binder import CypherBinder
from cycli.neo4j import Neo4j
from cycli.table import pretty_print_table
from cycli.cypher import Cypher


cypher = Cypher()


def get_tokens(x):
        return [(Token.Prompt, "> ")]


class Cycli:

    def __init__(self, host, port, username, password, logfile, filename, ssl, read_only):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.logfile = logfile
        self.filename = filename
        self.ssl = ssl
        self.read_only = read_only

    def write_to_logfile(self, query, response):
        results = response["results"]
        duration = response["duration"]
        error = response["error"]

        self.logfile.write("> {}\n".format(query))
        self.logfile.write("{}\n".format(results))

        if not error:
            self.logfile.write("{} ms\n\n".format(duration))

    def run(self):
        neo4j = Neo4j(self.host, self.port, self.username, self.password, self.ssl)
        neo4j.connect()
        self.neo4j = neo4j

        try:
            labels = neo4j.labels()
            relationship_types = neo4j.relationship_types()
            properties = neo4j.properties()

        except Unauthorized:
            print("Unauthorized. See cycli --help for authorization instructions.")
            return

        except SocketError:
            print("Connection refused. Is Neo4j turned on?")
            return

        if self.filename:
            queries = self.filename.read()
            queries = queries.split(";")[:-1]

            for query in queries:
                query += ";"
                query = query.strip()

                print("> " + query)
                self.handle_query(query)
                print()

            return

        click.secho(" ______     __  __     ______     __         __    ", fg="red")
        click.secho("/\  ___\   /\ \_\ \   /\  ___\   /\ \       /\ \   ", fg="yellow")
        click.secho("\ \ \____  \ \____ \  \ \ \____  \ \ \____  \ \ \  ", fg="green")
        click.secho(" \ \_____\  \/\_____\  \ \_____\  \ \_____\  \ \_\ ", fg="blue")
        click.secho("  \/_____/   \/_____/   \/_____/   \/_____/   \/_/ ", fg="magenta")

        print("\nVersion: {}".format(__version__))
        print("Bug reports: https://github.com/nicolewhite/cycli/issues\n")

        completer = CypherCompleter(labels, relationship_types, properties)

        layout = create_default_layout(
            lexer=CypherLexer,
            get_prompt_tokens=get_tokens,
            reserve_space_for_menu=True
        )

        buff = CypherBuffer(
            history=History(),
            completer=completer,
            complete_while_typing=Always()
        )

        application = Application(
            style=CypherStyle,
            buffer=buff,
            layout=layout,
            on_exit=AbortAction.RAISE_EXCEPTION,
            key_bindings_registry=CypherBinder.registry
        )

        cli = CommandLineInterface(application=application, eventloop=create_eventloop())

        try:
            while True:
                document = cli.run()
                query = document.text
                self.handle_query(query)

        except Exception:
            print("Goodbye!")

    def handle_query(self, query):
        # Check to see if the user is in run-n mode.
        m = re.match('run-([0-9]+) (.*)', query, re.DOTALL)

        if cypher.is_a_write_query(query) and self.read_only:
            print("Query aborted. You are in read-only mode.")

        elif query in ["quit", "exit"]:
            raise Exception

        elif query == "help":
            print_help()

        elif query == "refresh":
            self.neo4j.refresh()

        elif query == "schema":
            self.neo4j.print_schema()

        elif query == "schema-indexes":
            self.neo4j.print_indexes()

        elif query == "schema-constraints":
            self.neo4j.print_constraints()

        elif query == "schema-labels":
            self.neo4j.print_labels()

        elif query == "schema-rels":
            self.neo4j.print_relationship_types()

        else:
            count = int(m.group(1)) if m else 1
            query = m.group(2) if m else query

            if count <= 0 or not query:
                raise Exception

            total_duration = 0
            index = 0
            error = False

            while index < count:
                response = self.neo4j.cypher(query)

                results = response["results"]
                duration = response["duration"]
                error = response["error"]

                print(results)

                if not error:
                    ms = "Run {}: {} ms\n".format(index + 1, duration) if m else "{} ms".format(duration)
                    print(ms)

                if self.logfile:
                    self.write_to_logfile(query, response)

                total_duration += duration
                index += 1

            if m and not error:
                print("Total duration: {} ms".format(total_duration))


def print_help():
    headers = ["Keyword", "Description"]

    rows = [
        ["quit", "Exit cycli."],
        ["exit", "Exit cycli."],
        ["help", "Display this text."],
        ["refresh", "Refresh schema cache."],
        ["run-n", "Run a Cypher query n times."],
        ["schema", "Display indexes, constraints, labels, and relationship types."],
        ["schema-indexes", "Display indexes."],
        ["schema-constraints", "Display constraints."],
        ["schema-labels", "Display labels."],
        ["schema-rels", "Display relationship types."],
        ["CTRL-D", "Exit cycli if the input is blank."],
        ["CTRL-C", "Abort and rollback the currently-running query."]
    ]

    pretty_print_table(headers, rows)


@click.command()
@click.option("-v", "--version", is_flag=True, help="Show cycli version and exit.")
@click.option("-h", "--host", default="localhost", help="The host address of Neo4j.")
@click.option("-P", "--port", default="7474", help="The port number on which Neo4j is listening.")
@click.option("-u", "--username", help="Username for Neo4j authentication.")
@click.option("-p", "--password", help="Password for Neo4j authentication.")
@click.option("-t", "--timeout", help="Set a global socket timeout for queries.", type=click.INT)
@click.option('-l', '--logfile', type=click.File(mode="a", encoding="utf-8"), help="Log every query and its results to a file.")
@click.option("-f", "--filename", type=click.File(mode="rb"), help="Execute semicolon-separated Cypher queries from a file.")
@click.option("-s", "--ssl", is_flag=True, help="Use the HTTPS protocol.")
@click.option("-r", "--read-only", is_flag=True, help="Do not allow any write queries.")
def run(host, port, username, version, timeout, password, logfile, filename, ssl, read_only):
    if version:
        print("cycli {}".format(__version__))
        sys.exit(0)

    if username and not password:
        password = click.prompt("Password", hide_input=True, show_default=False, type=str)

    if timeout:
        http.socket_timeout = timeout

    cycli = Cycli(host, port, username, password, logfile, filename, ssl, read_only)
    cycli.run()


if __name__ == '__main__':
    run()