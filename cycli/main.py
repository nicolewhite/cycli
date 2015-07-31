from __future__ import unicode_literals

from prompt_toolkit.contrib.completers import WordCompleter
from prompt_toolkit.shortcuts import get_input
from prompt_toolkit.history import History
from pygments.lexers.graph import CypherLexer

import neo4j
import cypher

words = neo4j.words + cypher.words

completer = WordCompleter(words, ignore_case=True, match_middle=True)

def run():
    print "~~~ Welcome to cycli! ~~~\n"

    history = History()

    while True:
        query = get_input("> ", completer=completer, history=history, lexer=CypherLexer)

        if query == "quit":
            break

        while not query.endswith(";"):
            query += " "
            query += get_input("> ", completer=completer, history=history, lexer=CypherLexer)

        try:
            results = neo4j.graph.cypher.execute(query)
        except Exception as e:
            results = e

        print results

    print "Goodbye!"

if __name__ == '__main__':
    run()