from __future__ import unicode_literals

from prompt_toolkit.contrib.completers import WordCompleter
from prompt_toolkit.shortcuts import get_input
from prompt_toolkit.history import History
from pygments.lexers.graph import CypherLexer

from py2neo import Graph

graph = Graph()
reltypes = graph.relationship_types
labels = graph.node_labels

reltypes = list(reltypes)
labels = list(labels)

props = []

for label in labels:
    query = "MATCH (n:{}) RETURN n LIMIT 1;".format(label)
    n = graph.cypher.execute_one(query)

    if not n:
        continue

    props.extend(n.properties.keys())

props = list(set(props))

funcs = ["abs", "acos", "allShortestPaths", "asin", "atan", "atan2", "avg", "ceil", "coalesce", "collect", "cos", "cot", "count", "degrees", "e", "endnode", "exp", "extract", "filter", "floor", "haversin", "head", "id", "keys", "labels", "last", "left", "length", "log", "log10", "lower", "ltrim", "max", "min", "node", "nodes", "percentileCont", "percentileDisc", "pi", "radians", "rand", "range", "reduce", "rel", "relationship", "relationships", "replace", "right", "round", "rtrim", "shortestPath", "sign", "sin", "split", "sqrt", "startnode", "stdev", "stdevp", "str", "substring", "sum", "tail", "tan", "timestamp", "toFloat", "toInt", "trim", "type", "upper"]
keywords = ["as", "asc", "ascending", "assert", "by", "case", "commit", "constraint", "create", "csv", "cypher", "delete", "desc", "descending", "distinct", "drop", "else", "end", "explain", "false", "fieldterminator", "foreach", "from", "headers", "in", "index", "is", "like", "limit", "load", "match", "merge", "null", "on", "optional", "order", "periodic", "profile", "remove", "return", "scan", "set", "skip", "start", "then", "true", "union", "unique", "unwind", "using", "when", "where", "with"]
preds = ["all", "and", "any", "has", "in", "none", "not", "or", "single", "xor"]

funcs = [x.upper() for x in funcs]
keywords = [x.upper() for x in keywords]
preds = [x.upper() for x in preds]

autos = reltypes + labels + props + funcs + keywords + preds

completer = WordCompleter(autos, ignore_case=True, match_middle=True)

def main():
    history = History()

    while True:
        query = get_input("> ", completer=completer, history=history, lexer=CypherLexer)

        while not query.endswith(";"):
            query += " "
            query += get_input("> ", completer=completer, history=history, lexer=CypherLexer)

        try:
            results = graph.cypher.execute(query)
        except Exception as e:
            results = e

        print results

    print "Goodbye!"

if __name__ == '__main__':
    main()