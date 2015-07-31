from __future__ import unicode_literals
from prompt_toolkit.contrib.completers import WordCompleter
from neo4j import neo4j_words
from cypher import cypher_words

words = neo4j_words + cypher_words

CypherCompleter = WordCompleter(words, ignore_case=True, match_middle=True)