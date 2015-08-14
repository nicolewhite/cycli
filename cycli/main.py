from __future__ import unicode_literals, print_function

from datetime import datetime

import sys
import click

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
from cycli.neo4j import Neo4j


def get_tokens(x):
        return [(Token.Prompt, "> ")]

class Cycli:

    def __init__(self, host, port, username, password, logfile, filename):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.logfile = logfile
        self.filename = filename

    def run(self):
        neo4j = Neo4j(self.host, self.port, self.username, self.password)

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
                print("{};\n".format(query))
                results = neo4j.cypher(query)
                print(results)

            return

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
            on_exit=AbortAction.RAISE_EXCEPTION
        )

        cli = CommandLineInterface(application=application, eventloop=create_eventloop())

        try:
            while True:
                document = cli.run()
                query = document.text

                if query in ["quit", "exit"]:
                    raise Exception

                elif query == "help":
                    print(help_text())

                else:
                    results = neo4j.cypher(query)
                    print(results)

                    if self.logfile:
                        self.logfile.write("\n{}\n".format(datetime.now()))
                        self.logfile.write("\n{}\n".format(query))
                        self.logfile.write("\n{}\n".format(results))

        except Exception:
            print("Goodbye!")


@click.command()
@click.option("-h", "--host", default="localhost", help="The host address of Neo4j.")
@click.option("-P", "--port", default="7474", help="The port number on which Neo4j is listening.")
@click.option("-u", "--username", default=False,
              help="Username for Neo4j authentication. If provided, you will be prompted for a password.")
@click.option("-v", "--version", is_flag=True, help="Show cycli version and exit.")
@click.option("-t", "--timeout", default=False, help="Set a global socket timeout for queries.", type=click.INT)
@click.option("-p", "--password", default=False, help="Password for Neo4j authentication.")
@click.option('-l', '--logfile', type=click.File(mode="a", encoding="utf-8"),
              help="Log every query and its results to a file.")
@click.option("-f", "--filename", type=click.File(mode="rb"),
              help="Execute semicolon separated Cypher queries from a file.")
def run(host, port, username, version, timeout, password, logfile, filename):
    if version:
        print("cycli {}".format(__version__))
        sys.exit(0)

    print("Version: {}".format(__version__))
    print("Bug reports: https://github.com/nicolewhite/cycli/issues\n")

    if username and not password:
        password = click.prompt("Password", hide_input=True, show_default=False, type=str)

    if timeout:
        http.socket_timeout = timeout

    cycli = Cycli(host, port, username, password, logfile, filename)
    cycli.run()


def help_text():
    options = {
        "quit": "Exit cycli.",
        "exit": "Exit cycli.",
        "help": "Display this text.",
        "CTRL-D": "Exit cycli if the input is blank.",
        "CTRL-C": "Abort and rollback the currently-running query."
    }

    keyword_column_size = max([len("keyword")] + [len(key) for key in options.keys()])
    description_column_size = max([len("description")] + [len(descrip) for descrip in options.values()])

    header = " | " + " | ".join(["keyword".ljust(keyword_column_size), "description".ljust(description_column_size)]) + " | \n"
    divider = " | " +  "-" * keyword_column_size + " | " + "-" * description_column_size + " | \n"

    text = ""

    for key, value in options.items():
        text += " | " + " | ".join([key.ljust(keyword_column_size), value.ljust(description_column_size)]) + " | \n"

    return header + divider + text


if __name__ == '__main__':
    run()