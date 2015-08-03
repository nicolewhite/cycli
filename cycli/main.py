from __future__ import unicode_literals

import sys

from prompt_toolkit import Application, CommandLineInterface, AbortAction
from prompt_toolkit.history import History
from prompt_toolkit.shortcuts import create_default_layout, create_eventloop
from prompt_toolkit.filters import Always

from pygments.token import Token
import click
from py2neo.error import Unauthorized
from py2neo.packages.httpstream import SocketError

from . import __version__
from lexer import CypherLexer
from style import CypherStyle
from completer import CypherCompleter
from buffer import CypherBuffer
from neo4j import Neo4j


def get_tokens(x):
        return [(Token.Prompt, "> ")]

class Cycli:

    def __init__(self, host, port, username, password):
        self.host = host
        self.port = port
        self.username = username
        self.password = password

    def run(self):
        neo4j = Neo4j(self.host, self.port, self.username, self.password)

        try:
            labels = neo4j.labels()
            relationship_types = neo4j.relationship_types()
            properties = neo4j.properties()

        except Unauthorized:
            print "Unauthorized. See cycli --help for authorization instructions."
            return

        except SocketError:
            print "Connection refused. Is Neo4j turned on?"
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

                results = neo4j.cypher(query)
                print results

        except Exception:
            print "Goodbye!"


@click.command()
@click.option("-h", "--host", default="localhost", help="The host address of Neo4j.")
@click.option("-p", "--port", default="7474", help="The port number on which Neo4j is listening.")
@click.option("-u", "--username", default=False,
              help="Username for Neo4j authentication. If provided, you will be prompted for a password.")
@click.option("-v", "--version", is_flag=True, help="Show cycli version and exit.")
def run(host, port, username, version):
    if version:
        print "cycli {}".format(__version__)
        sys.exit(0)

    print "Version: {}".format(__version__)
    print "Bug reports: https://github.com/nicolewhite/cycli/issues\n"

    password = None

    if username:
        password = click.prompt("Password", hide_input=True, show_default=False, type=str)

    cycli = Cycli(host, port, username, password)
    cycli.run()


if __name__ == '__main__':
    run()
