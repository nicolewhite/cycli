from __future__ import unicode_literals

from prompt_toolkit import Application, CommandLineInterface, AbortAction
from prompt_toolkit.history import History
from prompt_toolkit.shortcuts import create_default_layout, create_eventloop
from prompt_toolkit.filters import Always

from pygments.token import Token

from lexer import CypherLexer
from style import CypherStyle
from completer import CypherCompleter
from buffer import CypherBuffer
from neo4j import graph


def run():
    print "~~~ Welcome to cycli! ~~~\n"

    def get_tokens(x):
        return [(Token.Prompt, "> ")]

    layout = create_default_layout(lexer=CypherLexer, get_prompt_tokens=get_tokens, reserve_space_for_menu=True)
    buff = CypherBuffer(history=History(), completer=CypherCompleter(), complete_while_typing=Always())
    application = Application(style=CypherStyle, buffer=buff, layout=layout, on_exit=AbortAction.RAISE_EXCEPTION)
    cli = CommandLineInterface(application=application, eventloop=create_eventloop())

    try:
        while True:
            document = cli.run()
            query = document.text

            if query == "quit;":
                raise Exception

            try:
                result = graph.cypher.execute(query)
            except Exception as e:
                result = e

            print result

    except Exception:
        print "Goodbye!"


if __name__ == '__main__':
    run()
