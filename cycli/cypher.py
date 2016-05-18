from cycli.markov import markov
import re

class Cypher:

    def __init__(self):
        self.FUNCTIONS = [
            "abs",
            "acos",
            "all",
            "allShortestPaths",
            "any",
            "asin",
            "atan",
            "atan2",
            "avg",
            "ceil",
            "coalesce",
            "collect",
            "cos",
            "cot",
            "count",
            "degrees",
            "e",
            "endNode",
            "exists",
            "exp",
            "extract",
            "filter",
            "floor",
            "has",
            "haversin",
            "head",
            "id",
            "keys",
            "labels",
            "last",
            "left",
            "length",
            "log",
            "log10",
            "lower",
            "ltrim",
            "max",
            "min",
            "node",
            "nodes",
            "none",
            "percentileCont",
            "percentileDisc",
            "pi",
            "radians",
            "rand",
            "range",
            "reduce",
            "rel",
            "relationship",
            "relationships",
            "replace",
            "reverse",
            "right",
            "round",
            "rtrim",
            "shortestPath",
            "sign",
            "sin",
            "single",
            "size",
            "split",
            "sqrt",
            "startNode",
            "stdev",
            "stdevp",
            "str",
            "substring",
            "sum",
            "tail",
            "tan",
            "timestamp",
            "toFloat",
            "toInt",
            "trim",
            "type",
            "upper"
        ]

        self.KEYWORDS = [
            "AND",
            "AS",
            "ASC",
            "ASCENDING",
            "ASSERT",
            "BY",
            "CASE",
            "COMMIT",
            "CONSTRAINT",
            "CONTAINS",
            "CREATE",
            "CSV",
            "CYPHER",
            "DELETE",
            "DESC",
            "DESCENDING",
            "DETACH",
            "DISTINCT",
            "DROP",
            "ELSE",
            "END",
            "ENDS",
            "EXPLAIN",
            "FALSE",
            "FIELDTERMINATOR",
            "FOREACH",
            "FROM",
            "HEADERS",
            "IN",
            "INDEX",
            "IS",
            "LIMIT",
            "LOAD",
            "MATCH",
            "MERGE",
            "NOT",
            "NULL",
            "ON",
            "OPTIONAL",
            "OR",
            "ORDER",
            "PERIODIC",
            "PROFILE",
            "REMOVE",
            "RETURN",
            "SCAN",
            "SET",
            "SKIP",
            "START",
            "STARTS",
            "THEN",
            "TRUE",
            "UNION",
            "UNIQUE",
            "UNWIND",
            "USING",
            "WHEN",
            "WHERE",
            "WITH",
            "XOR"
        ]

        self.markov = markov

    def words(self):
        return sorted(self.FUNCTIONS + self.KEYWORDS)

    def most_probable_next_keyword(self, current_keyword):
        return [x[0] for x in self.markov[current_keyword]]

    def is_a_write_query(self, query):
        query = query.upper()
        update_words = ["CREATE", "MERGE", "DELETE", "SET", "REMOVE", "DROP"]

        unquoted = re.findall('(?:^|"|\'|`)([^"|\'|`]*)(?:$|"|\'|`)', query, flags=re.DOTALL)
        unquoted = " " + "".join(unquoted) + " "
        unquoted = unquoted.replace("\n", " ")
        unquoted = unquoted.replace("\r", " ")
        unquoted = unquoted.replace("\t", " ")

        sightings = [unquoted.find(" " + word + " ") for word in update_words]

        return any([x > -1 for x in sightings])
