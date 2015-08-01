from __future__ import unicode_literals

from prompt_toolkit import Application, CommandLineInterface, AbortAction
from prompt_toolkit.history import History
from prompt_toolkit.shortcuts import create_default_layout, create_eventloop
from prompt_toolkit.filters import Always
from pygments.token import Token
import click

from lexer import CypherLexer
from style import CypherStyle
from completer import CypherCompleter
from buffer import CypherBuffer
from neo4j import Neo4j

def get_tokens(x):
        return [(Token.Prompt, "> ")]

class Cycli:

    def __init__(self, host, port):
        self.host = host
        self.port = port

    def run(self):
        neo4j = Neo4j(self.host, self.port)

        labels = neo4j.labels()
        relationship_types = neo4j.relationship_types()
        properties = neo4j.properties()

        completer = CypherCompleter(labels, relationship_types, properties)

        layout = create_default_layout(lexer=CypherLexer, get_prompt_tokens=get_tokens, reserve_space_for_menu=True)
        buff = CypherBuffer(history=History(), completer=completer, complete_while_typing=Always())
        application = Application(style=CypherStyle, buffer=buff, layout=layout, on_exit=AbortAction.RAISE_EXCEPTION)
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
def run(host, port):
    print "~~~ Welcome to cycli! ~~~\n"
    cycli = Cycli(host, port)
    cycli.run()


if __name__ == '__main__':
    run()
