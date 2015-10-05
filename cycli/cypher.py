from cycli.markov import markov
import re

class Cypher:

    def __init__(self):
        self.FUNCTIONS = [
            "ABS",
            "ACOS",
            "ALL",
            "ALLSHORTESTPATHS",
            "ANY",
            "ASIN",
            "ATAN",
            "ATAN2",
            "AVG",
            "CEIL",
            "COALESCE",
            "COLLECT",
            "COS",
            "COT",
            "COUNT",
            "DEGREES",
            "E",
            "ENDNODE",
            "EXP",
            "EXTRACT",
            "FILTER",
            "FLOOR",
            "HAS",
            "HAVERSIN",
            "HEAD",
            "ID",
            "KEYS",
            "LABELS",
            "LAST",
            "LEFT",
            "LENGTH",
            "LOG",
            "LOG10",
            "LOWER",
            "LTRIM",
            "MAX",
            "MIN",
            "NODE",
            "NODES",
            "NONE",
            "PERCENTILECONT",
            "PERCENTILEDISC",
            "PI",
            "RADIANS",
            "RAND",
            "RANGE",
            "REDUCE",
            "REL",
            "RELATIONSHIP",
            "RELATIONSHIPS",
            "REPLACE",
            "RIGHT",
            "ROUND",
            "RTRIM",
            "SHORTESTPATH",
            "SIGN",
            "SIN",
            "SINGLE",
            "SPLIT",
            "SQRT",
            "STARTNODE",
            "STDEV",
            "STDEVP",
            "STR",
            "SUBSTRING",
            "SUM",
            "TAIL",
            "TAN",
            "TIMESTAMP",
            "TOFLOAT",
            "TOINT",
            "TRIM",
            "TYPE",
            "UPPER"
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
            "CREATE",
            "CSV",
            "CYPHER",
            "DELETE",
            "DESC",
            "DESCENDING",
            "DISTINCT",
            "DROP",
            "ELSE",
            "END",
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