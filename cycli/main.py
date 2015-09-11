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


def get_tokens(x):
        return [(Token.Prompt, "> ")]

class Cycli:

    def __init__(self, host, port, username, password, logfile, filename, ssl):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.logfile = logfile
        self.filename = filename
        self.ssl = ssl

    def write_to_logfile(self, query, results, duration):
        self.logfile.write("{}\n".format(datetime.now()))
        self.logfile.write("\n{}\n".format(query))
        self.logfile.write("\n{}\n".format(results))
        self.logfile.write("{} ms\n\n".format(duration))

    def run(self):
        neo4j = Neo4j(self.host, self.port, self.username, self.password, self.ssl)
        neo4j.connect()

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

                results, duration = neo4j.cypher(query)

                print("{}\n".format(query))
                print(results)
                print("{} ms\n".format(duration))

                if self.logfile:
                    self.write_to_logfile(query, results, duration)

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

                m = re.match('run-([0-9]+) (.*)', query, re.DOTALL)

                if query in ["quit", "exit"]:
                    raise Exception

                elif query == "help":
                    print_help()

                elif query == "refresh":
                    neo4j.refresh()

                elif query == "schema":
                    neo4j.print_schema()

                elif query == "schema-indexes":
                    neo4j.print_indexes()

                elif query == "schema-constraints":
                    neo4j.print_constraints()

                elif query == "schema-labels":
                    neo4j.print_labels()

                elif query == "schema-rels":
                    neo4j.print_relationship_types()

                elif m:
                    count = int(m.group(1))
                    cypher = m.group(2)

                    if count <= 0 or not cypher:
                        raise Exception

                    total_duration = 0

                    index = 0
                    while index < count:
                        results, duration = neo4j.cypher(cypher)
                        total_duration += duration

                        print(results)
                        print("Run-{} : {} ms".format(index+1, duration))
                        print()

                        if self.logfile:
                            self.write_to_logfile(query, results, duration)

                        index += 1

                    print("Total duration: {} ms".format(total_duration))

                else:
                    results, duration = neo4j.cypher(query)
                    print(results)
                    print("{} ms".format(duration))

                    if self.logfile:
                        self.write_to_logfile(query, results, duration)

        except Exception:
            print("Goodbye!")


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
def run(host, port, username, version, timeout, password, logfile, filename, ssl):
    if version:
        print("cycli {}".format(__version__))
        sys.exit(0)

    if username and not password:
        password = click.prompt("Password", hide_input=True, show_default=False, type=str)

    if timeout:
        http.socket_timeout = timeout

    cycli = Cycli(host, port, username, password, logfile, filename, ssl)
    cycli.run()


def print_help():
    headers = ["Keyword", "Description"]

    rows = [
        ["quit", "Exit cycli."],
        ["exit", "Exit cycli."],
        ["help", "Display this text."],
        ["refresh", "Refreshes schema cache"],
        ["run-n", "Runs given cypher n-times."],
        ["schema", "Shows all index, constraints, labels, relations"],
        ["schema-indexes", "Shows all indexes."],
        ["schema-constraints", "Shows all constraints."],
        ["schema-labels", "Shows all labels."],
        ["schema-rels", "Shows all relationship types."],
        ["CTRL-D", "Exit cycli if the input is blank."],
        ["CTRL-C", "Abort and rollback the currently-running query."]
    ]

    pretty_print_table(headers, rows)


if __name__ == '__main__':
    run()