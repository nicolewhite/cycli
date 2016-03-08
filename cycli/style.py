import re

from pygments.lexer import RegexLexer
from pygments.token import Comment, Operator, Keyword, Name, String, Number, Token
from pygments.style import Style

__all__ = ["CypherLexer"]


class CypherLexer(RegexLexer):
    name = 'Cypher'
    aliases = ['cypher']
    filenames = ['*.cyp', '*.cypher']

    flags = re.IGNORECASE

    tokens = {
        'root': [
            (r'//.*?\n', Comment.Single),
            (r'\b(ABS|ACOS|ALL|ALLSHORTESTPATHS|AND|ANY|AS|ASC|ASCENDING|ASIN|ASSERT|ATAN|ATAN2|AVG'
             r'|BY'
             r'|CASE|CEIL|COALESCE|COLLECT|COMMIT|CONSTRAINT|CONTAINS|COS|COT|COUNT|CREATE|CYPHER'
             r'|DEGREES|DELETE|DESC|DESCENDING|DETACH|DISTINCT|DROP'
             r'|E|ELSE|END|ENDNODE|ENDS|EXISTS|EXP|EXPLAIN|EXTRACT'
             r'|FALSE|FIELDTERMINATOR|FILTER|FLOOR|FOREACH|FROM'
             r'|HAS|HAVERSIN|HEAD|HEADERS'
             r'|ID|ILIKE|IN|INDEX|IS'
             r'|KEYS'
             r'|LABELS|LAST|LEFT|LENGTH|LIKE|LIMIT|LOAD CSV|LOG|LOG10|LOWER|LTRIM'
             r'|MATCH|MAX|MERGE|MIN'
             r'|NODE|NODES|NONE|NOT|NULL'
             r'|ON|OPTIONAL|OR|ORDER'
             r'|PERCENTILECONT|PERCENTILEDISC|PERIODIC|PI|PROFILE'
             r'|RADIANS|RAND|RANGE|REDUCE|REL|RELATIONSHIP|RELATIONSHIPS|REMOVE|REPLACE|RETURN|REVERSE|RIGHT|ROUND|RTRIM'
             r'|SCAN|SET|SHORTESTPATH|SIGN|SIN|SINGLE|SIZE|SKIP|SPLIT|SQRT|START|STARTNODE|STARTS|STDEV|STDEVP|STR|SUBSTRING|SUM'
             r'|TAIL|TAN|THEN|TIMESTAMP|TOFLOAT|TOINT|TRIM|TRUE|TYPE'
             r'|UNION|UNIQUE|UNWIND|USING|UPPER'
             r'|WHEN|WHERE|WITH'
             r'|XOR)\b', Keyword),
            (r'[+*/<>=~!@#%^&|`?-]', Operator),
            (r'quit|exit|help|refresh|run-[0-9]+|save-csv|schema|schema-constraints|schema-indexes|schema-labels|schema-rels|env|export', Number),
            (r'[0-9]+', Name),
            (r'[a-zA-Z_][a-zA-Z0-9_]*', Name),
            (r"'(''|[^'])*'", String.Single),
            (r'"(""|[^"])*"', String.Symbol),
            (r'[\]\)]-[\(\[]|[\]\)]->\(|\)<-[\[\(]|[\)\]]-->\(|\)<--[\(\[]|[\)\]]--[\(\[]', Token.Pattern),
            (r'\.', Token.Pattern),
            (r'\(|\)|\]|\[|{|}', Token.Pattern),
        ]
    }


class CypherStyle(Style):
    styles = {
        Token.Keyword: '#3498DB',
        Token.String: '#E67E22',
        Token.Name: '#1ABC9C',
        Token.Pattern: '#E74C3C',
        Token.Number: '#BF5FFF',

        Token.Line: 'bg:#000000 #ffffff',

        Token.LineNumber: 'bg:#ffffaa #000000',
        Token.Menu.Completions.Completion.Current: 'bg:#00aaaa #000000',
        Token.Menu.Completions.Completion: 'bg:#008888 #ffffff',
        Token.Menu.Completions.ProgressButton: 'bg:#003333',
        Token.Menu.Completions.ProgressBar: 'bg:#00aaaa',

        Token.Toolbar.Completions: 'bg:#888800 #000000',
        Token.Toolbar.Completions.Arrow: 'bg:#888800 #000000',
        Token.Toolbar.Completions.Completion: 'bg:#aaaa00 #000000',
        Token.Toolbar.Completions.Completion.Current: 'bg:#ffffaa #000000 bold',

        Token.AfterInput: 'bg:#ff44ff #000000',
    }
