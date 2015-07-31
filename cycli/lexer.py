import re
from pygments.lexer import RegexLexer
from pygments.token import Punctuation, Text, Comment, Operator, Keyword, Name, String, Number

__all__ = ["CypherLexer"]

class CypherLexer(RegexLexer):
    name = 'Cypher'
    aliases = ['cypher']
    filenames = ['*.cyp', '*.cypher']

    flags = re.IGNORECASE
    tokens = {
        'root': [
            (r'\s+', Text),
            (r'//.*?\n', Comment.Single),
            (r'\b(ABS|ACOS|ALLSHORTESTPATHS|ASIN|ATAN|ATAN2|AVG|CEIL|COALESCE|COLLECT'
             r'|COS|COT|COUNT|DEGREES|E|ENDNODE|EXP|EXTRACT|FILTER|FLOOR'
             r'|HAVERSIN|HEAD|ID|KEYS|LABELS|LAST|LEFT|LENGTH|LIKE|LOAD CSV|LOG|LOG10'
             r'|LOWER|LTRIM|MAX|MIN|NODE|NODES|PERCENTILECONT|PERCENTILEDISC|PI|RADIANS'
             r'|RAND|RANGE|REDUCE|REL|RELATIONSHIP|RELATIONSHIPS|REPLACE|RIGHT|ROUND|RTRIM'
             r'|SHORTESTPATH|SIGN|SIN|SPLIT|SQRT|STARTNODE|STDEV|STDEVP|STR|SUBSTRING'
             r'|SUM|TAIL|TAN|TIMESTAMP|TOFLOAT|TOINT|TRIM|TYPE|UPPER|ALL'
             r'|AND|ANY|HAS|IN|NONE|NOT|OR|SINGLE|XOR|AS'
             r'|ASC|ASCENDING|ASSERT|BY|CASE|COMMIT|CONSTRAINT|CREATE|CYPHER'
             r'|DELETE|DESC|DESCENDING|DISTINCT|DROP|ELSE|END|EXPLAIN|FALSE|FIELDTERMINATOR'
             r'|FOREACH|FROM|WITH HEADERS|IN|INDEX|IS|LIMIT|LOAD|MATCH|MERGE'
             r'|NULL|ON|OPTIONAL|ORDER|PERIODIC|PROFILE|REMOVE|RETURN|SCAN|SET'
             r'|SKIP|START|THEN|TRUE|UNION|UNIQUE|UNWIND|USING|WHEN|WHERE|WITH)\b', Keyword),
            (r'[+*/<>=~!@#%^&|`?-]', Operator),
            (r'[0-9]+', Number.Integer),
            (r"'(''|[^'])*'", String.Single),
            (r'"(""|[^"])*"', String.Symbol),
            (r'[a-zA-Z_][a-zA-Z0-9_]*', Name),
            (r'[;:()\[\],\.]', Punctuation)
        ]
    }